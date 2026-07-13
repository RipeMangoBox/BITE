---
title: Bailando 3D Dance Generation by Actor Critic GPT with Choreographic Memory
type: paper
paper_level: A
venue: TPAMI
year: 2023
pdf_ref: paperPDFs/TPAMI_2023/Bailando_3D_Dance_Generation_by_Actor_Critic_GPT_with_Choreographic_Memory.pdf
project_link: null
code_link: https://github.com/karpathy/
aliases:
- B3DGBACGCM
tags:
- TPAMI_2023
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
- topic/benchmarks_datasets_evaluation
core_operator: 利用VQ-VAE构建的编排记忆（离散姿态码本）约束姿态质量，并通过演员-评论家强化学习微调GPT，使用节拍对齐奖励函数同步运动节奏与音乐节拍。
primary_logic: 将舞蹈生成分解为从音乐和过去姿态序列中自回归预测上下半身分离的离散姿态代码，结合跨条件因果注意力保持身体协调，并通过混合训练策略实现旋转域输出，兼顾空间质量与人体形态约束。
claims:
- Bailando++在AIST++测试集上的FIDk达到17.59，显著优于FACT的35.35等基线，用户研究中以≥88.5%胜率领先。
- 消融实验表明量化（编排记忆）至关重要：去除量化后FIDg剧增135.41；跨条件注意力去除后FIDk下降8.66（30%）。
- 混合训练策略对旋转域生成必不可少：未使用混合训练时，FIDk下降8.71（30%）且无法完成复杂转身动作。
- AIST++ test set 上 FIDk ↓ = 17.59
---

# Bailando 3D Dance Generation by Actor Critic GPT with Choreographic Memory

> [!tip] 核心洞察
> 将舞蹈生成分解为从音乐和过去姿态序列中自回归预测上下半身分离的离散姿态代码，结合跨条件因果注意力保持身体协调，并通过混合训练策略实现旋转域输出，兼顾空间质量与人体形态约束。

| 字段 | 内容 |
|------|------|
| 中文题名 | Bailando++：基于编排记忆的3D舞蹈GPT |
| 英文题名 | Bailando 3D Dance Generation by Actor Critic GPT with Choreographic Memory |
| 会议/期刊 | TPAMI 2023 |
| Links | [paper](https://arxiv.org/abs/2301.09036) · [Code](https://github.com/karpathy/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion #topic/benchmarks_datasets_evaluation |
| Method | Bailando++ |
| Dataset | AIST++ test set, User Study |

> [!tip] 效果简介
> - AIST++ test set 上，FIDk ↓ 17.59 vs 35.35 (FACT) (-17.76 (↓50.3%))；FIDg ↓ 10.10 vs 22.11 (FACT) (-12.01 (↓54.3%))；Beat Align Score ↑ 0.2720 vs 0.2109 (w/o actor-critic) (+0.0611 (↑29%))。
> - User Study 上，Win Rate vs Bailando (CVPR2022) 78.0% vs 22.0% (remainder / 50% random) (78% wins)。

## 概要

**核心问题**：现有3D舞蹈生成方法通常直接从音乐映射到连续的3D关节位置空间，难以显式约束舞蹈姿态的空间质量，且在与多样化音乐节拍保持时间一致性方面存在瓶颈。此外，基于3D关节位置的输出需要借助逆运动学（IK）转换为关节旋转角才能驱动虚拟人，这一过程常引入人体形态失真和脚部滑步等伪影。

**核心思路**：Bailando++提出了一套“离散记忆编码—自回归生成—强化学习微调”的舞蹈生成框架。其核心洞察在于将舞蹈生成分解为两个阶段：（1）利用VQ-VAE从标准舞蹈动作中学习一个离散的**编排记忆（Choreographic Memory）**，将上下半身姿态分别量化为有限的姿态码本，以此约束生成姿态的空间质量；（2）通过一个带有**跨条件因果注意力**的Motion GPT，以音乐特征和起始姿态码为条件，自回归地预测未来的上下半身姿态代码对。在此基础上，引入**演员-评论家强化学习**对GPT进行微调，使用节拍对齐奖励和半身一致性奖励来同步运动节奏与音乐节拍。为支持旋转域输出，Bailando++还设计了**混合训练策略**：先在3D位置域训练VQ-VAE编码器和码本，再冻结编码器/码本并训练旋转角解码器，从而在保证空间质量的同时直接生成SMPL关节旋转角，避免IK转换带来的形态失真。

**方法定位**：Bailando++在方法谱系上属于“基于离散码本的GPT式舞蹈生成 + 强化学习微调”。其前身Bailando（Siyao et al., CVPR 2022 oral）已采用VQ-VAE码本和GPT架构，但输出为3D关节位置且缺乏旋转域训练。Bailando++在此基础上进行了三项关键升级：（1）输出从3D位置升级为SMPL关节旋转角；（2）引入混合训练策略使VQ-VAE同时受益于位置域和旋转域；（3）引入演员-评论家强化学习微调，显式优化节拍对齐。相较于FACT（Li et al., ICCV 2021）、DanceFormer（Li et al., AAAI 2022）等基于Transformer的直接回归方法，以及EDGE（Tseng et al., CVPR 2023）等扩散模型方法，Bailando++的核心差异在于通过离散码本约束姿态空间质量，并通过强化学习显式注入节拍对齐先验。

**主要结果**：在AIST++测试集上，Bailando++的FIDk达到17.59，较FACT的35.35降低约50%；FIDg达到10.10，较FACT的22.11降低约54%。消融实验表明：去除量化（编排记忆）后FIDg飙升至145.51（↑135.41），证明离散码本对姿态质量的约束至关重要；去除跨条件因果注意力后FIDk增加30%；去除混合训练策略后旋转域FIDk增加122%且无法完成转身动作。用户研究中，Bailando++以≥88.5%的胜率领先于所有对比方法。



3D舞蹈生成的核心任务是根据给定的音乐片段，自动合成与之在节奏、风格和结构上高度契合的3D人体舞蹈动作序列。这一任务在虚拟人动画、游戏开发和数字内容创作中具有广泛的应用前景。然而，高质量舞蹈生成面临两大根本性瓶颈：**空间质量约束**与**时间一致性对齐**。

在空间维度上，现有方法通常直接从音乐特征映射到连续的3D关节位置空间（如**FACT**，Li et al., ICCV 2021；**DanceFormer**，Li et al., AAAI 2022），或通过扩散模型生成动作（如**EDGE**，Tseng et al., CVPR 2023）。这类连续回归范式缺乏对舞蹈姿态空间质量的显式约束，容易产生违反人体形态学规律的异常姿态。此外，3D关节位置输出往往需要经过逆运动学（IK）转换才能驱动虚拟人，这一后处理步骤会引入额外的形态失真——例如下蹲时膝盖穿透身体、转身时脚部滑步等问题（Fig. 3）。

在时间维度上，音乐与舞蹈的节拍同步是评估生成质量的关键主观指标。然而，多数现有方法并未显式建模音乐节拍与舞蹈动作节拍之间的对齐关系，导致生成的舞蹈在节奏上缺乏“卡点感”，难以满足专业编舞需求。

为应对上述挑战，**Bailando++** 提出了一套全新的舞蹈生成范式，其核心思想是将舞蹈生成问题分解为三个子任务：首先，利用VQ-VAE构建**编排记忆**（Choreographic Memory），将连续姿态空间量化为离散的、具有编舞语义的姿态码本，从源头上约束姿态质量；其次，通过**Motion GPT**自回归地预测上下半身分离的离散姿态代码，实现音乐到舞蹈的结构化翻译；最后，引入**演员-评论家强化学习**微调机制，使用节拍对齐奖励函数显式优化运动节奏与音乐节拍的时间一致性。此外，Bailando++升级了输出表示，从3D关节位置转向SMPL关节旋转角度域，可直接驱动虚拟人，并通过混合训练策略解决了旋转域生成中的空间质量退化问题。



## 核心方法与创新机理

Bailando++ 的核心创新在于将舞蹈生成从“音乐→连续关节位置”的直接映射，重构为“音乐→离散姿态代码→旋转角序列”的分层生成范式，通过三个关键机制解决了现有方法的根本性瓶颈。

### 瓶颈与因果调节变量

现有舞蹈生成方法（如 **FACT** (Li et al., ICCV 2021)、**DanceFormer** (Li et al., AAAI 2022)、**EDGE** (Tseng et al., CVPR 2023)）面临两个核心瓶颈：其一，直接从音乐映射到连续的3D关节位置空间，缺乏对姿态空间质量的显式约束，生成的动作易出现不自然的扭曲或抖动；其二，难以与多样化的音乐节拍保持时间一致性，舞蹈节奏与音乐节拍之间常出现错位。

Bailando++ 的**因果调节变量**是：利用 VQ-VAE 构建的**编排记忆**（离散姿态码本）约束姿态质量，并通过**演员-评论家强化学习**微调 GPT，使用节拍对齐奖励函数同步运动节奏与音乐节拍。这一设计将生成问题分解为“从音乐和过去姿态序列中自回归预测上下半身分离的离散姿态代码”，结合跨条件因果注意力保持身体协调，并通过混合训练策略实现旋转域输出，兼顾空间质量与人体形态约束。

### 相对基线方法的关键创新（Changed Slots）

与基线方法相比，Bailando++ 在四个关键维度上进行了系统性改进：

**1. 输出姿态表示：从3D位置到SMPL关节旋转角度**

基线方法（包括 Bailando 前身版本，Siyao et al., CVPR 2022 oral）生成3D关节位置，需通过逆运动学（IK）转换为旋转角度才能驱动虚拟人，这一过程常引入形态失真和脚部滑动等误差（见 Fig. 3）。Bailando++ 直接生成 SMPL 格式的关节旋转角度，可直接驱动虚拟人，从根本上避免了 IK 转换带来的误差累积。然而，直接在旋转域训练 VQ-VAE 不可行——旋转空间中的距离度量与空间姿态差异不匹配，导致码本学习失败。为此，论文提出了**混合训练策略**（见下文第3点）来解决这一难题。

**2. 姿态空间建模：从连续回归到离散量化的编排记忆**

基线方法在连续空间中进行回归或使用手动裁剪的动作片段，缺乏对“什么是高质量舞蹈姿态”的显式建模。Bailando++ 的核心创新是引入**编排记忆**——通过 VQ-VAE 将上下半身的3D姿态分别编码为离散码本 $\mathcal{Z}^u$ 和 $\mathcal{Z}^l$。每个码本元素代表一种独特的舞蹈姿态，码本的有穷性天然约束了生成姿态的质量下限。消融实验证实了这一设计的决定性作用：去除量化后，FIDg 从 10.10 飙升至 145.51（↑135.41），表明连续空间中的生成严重缺乏质量约束（Table V）。此外，Fig. 11 展示了码本的可解释性：单个代码解码为静态姿态，两个不同代码解码为姿态间的平滑过渡，表明编排记忆确实学到了有意义的舞蹈单元。

**3. 音乐-运动对齐：从无显式约束到演员-评论家强化学习微调**

基线方法缺乏显式的节拍对齐机制，导致生成的舞蹈节奏与音乐节拍脱节。Bailando++ 设计了**演员-评论家强化学习框架**微调 Motion GPT，使用两类奖励函数：（a）**节拍对齐奖励**：惩罚音乐节拍区间内缺少舞蹈节拍的情况（Fig. 8a）；（b）**半身一致性奖励**：基于上下半身法线方向夹角计算，防止身体不同步（Fig. 8b）。消融实验表明，去除演员-评论家微调后，Beat Align Score 从 0.2720 降至 0.2264（↓17%），FIDk 上升 3.23（15%）（Table V/VI）。

**4. 音乐编码方式：从固定窗口FFT到上下文音乐编码器**

基线方法使用固定窗口的 FFT 特征，难以捕捉音乐的长程结构。Bailando++ 提出了**上下文音乐编码器**（Contextual Music Encoder, CME），通过带滑动窗口注意力的 Transformer 层增强音乐特征的长程依赖（Fig. 7）。消融实验显示，去除 CME 后 FIDk 上升 10.70（60%）至 28.29，FIDg 上升 2.61（26%）（Table VI），证实了长程音乐上下文对舞蹈生成质量的重要性。

### 混合训练策略：桥接位置域与旋转域

Bailando++ 的另一个关键创新是**混合训练策略**，这是实现旋转域生成的前提。直接在旋转角数据上训练 VQ-VAE 会失败，因为旋转空间的距离度量无法正确反映空间姿态差异。混合训练策略分两阶段进行：首先在3D位置域训练 VQ-VAE（编码器、码本、位置解码器），然后冻结编码器和码本，仅训练旋转角解码器（使用公式 $\mathcal{L}_{A}$ 约束角度及其一阶、二阶导数）。这一策略使得码本学习仍受益于位置空间的距离度量，同时输出可直接驱动虚拟人的旋转角序列。消融实验证实其必要性：未使用混合训练时，旋转域 FIDk 从 17.59 升至 39.09（↑122%），且无法完成转身等复杂动作（Table VI, Fig. 10）。

### 跨条件因果注意力：协调上下半身

Motion GPT 采用**跨条件因果注意力**（Cross-conditional Causal Attention, Fig. 6c），与标准因果注意力（Fig. 6b）不同，它在保持时间因果性的同时，允许当前时刻的上半身（或下半身）姿态预测同时关注：自身历史姿态、另一半身的历史姿态、以及当前及历史音乐特征。这种设计实现了上下半身的协调生成。消融实验表明，去除跨条件注意力后，FIDk 增加 8.66（30%）至 26.32，FIDg 增加 3.70（31%）（Table V），证实了跨半身信息交互对生成协调舞蹈动作的关键作用。

### 创新总结

Bailando++ 的创新可归纳为一条清晰的技术路线：**离散化姿态空间（编排记忆）→ 分层自回归生成（跨条件GPT）→ 强化学习精调（节拍对齐）→ 混合训练桥接域差异（旋转输出）**。这一路线使 Bailando++ 在 AIST++ 测试集上取得了 FIDk 17.59（FACT 的 35.35 降低 50.3%）、FIDg 10.10（FACT 的 22.11 降低 54.3%）的显著提升，并在用户研究中以 ≥88.5% 的胜率领先所有对比方法（Table I）。



Bailando++ 将舞蹈生成建模为一个从音乐到离散姿态代码的自回归翻译问题，其核心管线由三个级联的子系统构成：**姿态 VQ-VAE（编排记忆）**、**上下文音乐编码器（CME）** 与 **演员-评论家动作 GPT**。

**输入与输出流**：给定一段音乐音频，系统首先通过上下文音乐编码器提取具有长程依赖的音乐特征 $\mathbf{m}_{1\dots T}$。随后，演员-评论家动作 GPT 以自回归方式，根据当前音乐特征与过去的上/下半身姿态代码 $[p_{t-1}^u, p_{t-1}^l]$，预测下一时刻的上下半身姿态代码对 $[\hat{p}_t^u, \hat{p}_t^l]$。预测出的离散代码序列通过编排记忆嵌入为量化特征，最终由基于 CNN 的解码器重建为连续的 3D 舞蹈序列（Fig. 2）。

**模块关系与因果链路**：

1. **姿态 VQ-VAE 与编排记忆**：这是整个框架的质量约束瓶颈。上下半身各自独立的 VQ-VAE 将空间标准的 3D 舞蹈动作编码并量化为有限码本 $\mathcal{Z} = \{\mathbf{z}_i\}_{i=0}^{\bar{N}-1}$，称为“编排记忆”。这一离散化操作将舞蹈姿态空间压缩为可重用的舞蹈单元，从根本上约束了生成姿态的空间质量——消融实验中去除量化后，FIDg 从 10.10 飙升至 145.51（↑135.41），充分验证了其关键作用。

2. **混合训练策略**：为将输出从 3D 关节位置升级为可直接驱动虚拟人的 SMPL 关节旋转角，Bailando++ 引入混合训练策略：先在 3D 位置域训练 VQ-VAE 的编码器和码本，再冻结编码器/码本，单独训练旋转角解码器。这一设计解决了“旋转空间距离与空间姿态差异不匹配”的因果矛盾——若直接在旋转域训练 VQ-VAE，FIDk 会急剧下降 8.71（30%），且无法完成转身动作（Fig. 10）。

3. **跨条件因果注意力 GPT**：动作 GPT 的核心创新在于跨条件因果注意力机制。不同于标准因果注意力仅允许时间维度的单向依赖，Bailando++ 的注意力层在保持因果性的同时，允许上/下半身与音乐三类组件之间进行有向信息交互（Fig. 6）：上半身预测可条件于音乐、过去的上半身姿态和过去的下半身姿态；下半身预测同理。去除这一跨条件设计后，FIDk 上升 8.66（30%），FIDg 上升 3.70（31%），表明跨半身协调对运动质量至关重要。

![[assets/figures/papers/2023_Bailando_3D_Dance_Generation_by_Actor_Critic_GPT_with_Choreographic_Memory_cdf67d1d7f60/figures/006_Figure_6.jpg]]
*Figure 6: (a) Full attention (b) Causal attention (c) Cross-conditional causal attention Fig. 6. Different types of attention layers. The proposed cross-conditional causal attention realizes causal inferences intra (gray lines) and inter (blue lines) different kinds of components (gray and blue circles). Two kinds of components are shown here for concision, but three (music, upper, lower bodies) are in reality*

4. **上下文音乐编码器**：在进入 GPT 之前，音乐特征通过带滑动窗口注意力的 Transformer 层进行增强（Fig. 7），以在局部感受野内聚合相邻音乐特征，弥补标准帧级特征缺乏长程上下文的问题。去除 CME 会导致 FIDk 上升 10.70（60%）。

5. **演员-评论家微调**：GPT 先通过交叉熵损失 $\mathcal{L}_{CE}$ 进行监督预训练，再通过演员-评论家强化学习进行微调，使用节拍对齐奖励和半身一致性奖励（Fig. 8）直接优化运动-音乐节拍同步。微调后 Beat Align Score 从 0.2264 提升至 0.2720（↑20%）。

![[assets/figures/papers/2023_Bailando_3D_Dance_Generation_by_Actor_Critic_GPT_with_Choreographic_Memory_cdf67d1d7f60/figures/008_Figure_8.jpg]]
*Figure 8: Designed rewards. (a) Beat-align reward penalizes the absence of dance beat for the interval that has music beat. (b) Half-body consistency reward is computed on the angle between normal directions of half bodies to prevent asynchronizations*

**端到端流程**：音乐 → 上下文音乐编码 → 演员-评论家 GPT 自回归预测离散姿态代码对 → 编排记忆嵌入 → CNN 解码器重建 3D 旋转角序列 → 可直接驱动虚拟人的舞蹈动画。

### 补充图表

![[assets/figures/papers/2023_Bailando_3D_Dance_Generation_by_Actor_Critic_GPT_with_Choreographic_Memory_cdf67d1d7f60/figures/002_Figure_2.jpg]]
*Figure 2: Dance generation pipeline of Bailando++. Given a piece of music, an actor-critic motion GPT autoregressively predicts the future upper-lower pose code pairs according to the music features and starting pose codes. The pose code sequence is then embedded to quantized features via a learned choreographic memory and finally decoded into a dance sequence by a CNN-based decoder*



Bailando++ 的生成管线由四个核心模块串联构成：**姿态 VQ-VAE（编排记忆）**、**上下文音乐编码器**、**运动 GPT（跨条件因果注意力）** 以及 **演员-评论家强化学习微调**。各模块之间存在清晰的信息流依赖——VQ-VAE 负责将连续姿态空间压缩为离散码本，GPT 在此基础上自回归预测未来姿态码，音乐编码器为 GPT 提供长程音频上下文，而 RL 微调则在推理阶段注入节拍对齐与身体一致性约束。

### 3D 姿态 VQ-VAE 与编排记忆

该模块的目标是将空间标准化的舞蹈动作编码并量化为一个有限码本 $\mathcal{Z} = \{\mathbf{z}_i\}_{i=0}^{\bar{N}-1}$，即编排记忆（choreographic memory）。为扩大姿态表示范围，上下半身分别学习独立的 VQ-VAE 和码本 $\mathcal{Z}^u$、$\mathcal{Z}^l$。

**量化过程**通过最近邻查找实现：

$$\mathbf{e_{q,i}} = \arg\min_{\mathbf{z}_j \in \mathcal{Z}} \| \mathbf{e}_i - \mathbf{z}_j \| \tag{1}$$

其中 $\mathbf{e}_i$ 为编码器输出的第 $i$ 帧特征，$\mathbf{e_{q,i}}$ 为其在码本中的最近邻替代。码本损失和承诺损失的联合效应促使编码特征 $\mathbf{e}$ 向其最相似的码本元素 $\mathbf{z}_i$ 收敛，反之亦然，从而将相似编码特征聚类为可复用的姿态单元。

**VQ-VAE 总损失**由三部分构成：

$$\mathcal{L}_{VQ} = \mathcal{L}_{rec}(\hat{P}, P) + \| \mathrm{sg}[\mathbf{e}] - \mathbf{e_q} \| + \beta \| \mathbf{e} - \mathrm{sg}[\mathbf{e_q}] \| \tag{2}$$

其中 $\mathrm{sg}[\cdot]$ 为停止梯度算子，第二项为码本损失（推动码本元素靠近编码特征），第三项为承诺损失（推动编码特征靠近码本元素），$\beta$ 为权重系数。

**重建损失** $\mathcal{L}_{rec}$ 采用包含位置、速度和加速度的 L1 损失，以抑制生成舞蹈的抖动：

$$\mathcal{L}_{rec}(\hat{P}, P) = \| \hat{P} - P \|_1 + \alpha_1 \| \hat{P}' - P' \|_1 + \alpha_2 \| \hat{P}'' - P'' \|_1 \tag{3}$$

其中 $\hat{P}$ 和 $P$ 分别为重建姿态和真实姿态，$\hat{P}'$、$P'$ 为一阶导数（速度），$\hat{P}''$、$P''$ 为二阶导数（加速度），$\alpha_1$、$\alpha_2$ 为权重系数。消融实验证实，速度和加速度损失项对防止抖动至关重要。

**混合训练策略**：由于旋转空间中的距离度量与空间姿态差异不匹配，直接在旋转数据上训练 VQ-VAE 不可行。因此 Bailando++ 提出混合训练策略——先在 3D 位置域训练 VQ-VAE 的编码器和码本，随后冻结编码器和码本，仅训练旋转角解码器。旋转角解码器的损失函数与位置域类似：

$$\mathcal{L}_{A} = \| \hat{A} - A \|_{1} + \alpha_{1} \| \hat{A}^{\prime} - A^{\prime} \|_{1} + \alpha_{2} \| \hat{A}^{\prime\prime} - A^{\prime\prime} \|_{1} \tag{4}$$

其中 $\hat{A}$ 和 $A$ 分别为重建和真实的 SMPL 关节旋转角。该策略使模型既能利用位置域良好的空间聚类特性构建码本，又能输出可直接驱动虚拟人的旋转角序列。

此外，下半身码本还连接一个**全局速度解码器**，用于预测根关节的全局位移速度，从而恢复完整的全局运动轨迹。

### 上下文音乐编码器

音乐编码器采用基于注意力的 Transformer 结构，在滑动窗口内聚合相邻音乐特征以增强长程依赖。具体流程为：以 60 fps 采样长度为 $T + 2w$ 的音乐特征，送入级联的 Transformer 层，每层的注意力在宽度为 $(2w+1)$ 的滑动窗口内聚合相邻特征。增强后的特征最终通过时间维度的 unshuffling 操作下采样，与姿态序列的时间分辨率对齐。

### 运动 GPT 与跨条件因果注意力

运动 GPT 的核心任务是自回归地预测未来上下半身姿态码。给定音乐特征 $\mathbf{m}_{1\dots t}$ 和历史姿态码 $p_{0\dots t-1}^u$、$p_{0\dots t-1}^l$，模型预测下一时刻的上下半身姿态码：

$$\hat{p}_t^u = \arg\max_k \mathbb{P}(\mathbf{z}_k^u | \mathbf{m}_{1\dots t}, p_{0\dots t-1}^u, p_{0\dots t-1}^l)$$
$$\hat{p}_t^l = \arg\max_k \mathbb{P}(\mathbf{z}_k^l | \mathbf{m}_{1\dots t}, p_{0\dots t}^u, p_{0\dots t-1}^l)$$

注意下半身的预测额外条件于当前时刻已预测的上半身姿态码 $\hat{p}_t^u$，实现了上下半身的因果协调。

**跨条件因果注意力**是该模块的关键设计。与标准全注意力和因果注意力不同，跨条件因果注意力在三种成分（音乐、上半身、下半身）之间实现了组件内（intra）和组件间（inter）的因果推断。其数学形式为带掩码的缩放点积注意力：

$$\mathrm{Attention}(\mathbf{Q}, \mathbf{K}, \mathbf{V}, \mathbf{M}) = \mathrm{softmax}\left(\frac{\mathbf{Q}\mathbf{K}^T + \mathbf{M}}{\sqrt{C}}\right)\mathbf{V} \tag{6}$$

其中 $\mathbf{M}$ 为掩码矩阵，控制注意力流的因果方向——音乐可关注所有历史音乐特征，上半身可关注历史和当前音乐及自身历史，下半身可关注音乐、上半身当前及自身历史。这种设计既保证了时间因果性，又允许跨组件的信息交互以维持身体协调。

**GPT 的监督损失**为交叉熵：

$$\mathcal{L}_{CE} = \frac{1}{T'} \sum_{t=0}^{T'-1} \sum_{h=u,l} \mathrm{CrossEntropy}(\mathbf{a}_t^h, p_{t+1}^h) \tag{7}$$

其中 $\mathbf{a}_t^h$ 为模型输出的动作概率分布，$p_{t+1}^h$ 为真实下一帧姿态码。

### 演员-评论家强化学习微调

在监督预训练后，Bailando++ 引入演员-评论家框架对运动 GPT 进行微调。该框架包含三个网络：状态网络编码当前姿态码和音乐特征，策略网络（演员）输出动作概率，评论家网络估计状态价值。微调使用两类奖励函数：

- **节拍对齐奖励**：惩罚在音乐节拍区间内缺失舞蹈节拍的情况。当音乐节拍出现时，若最近邻的舞蹈运动学节拍（基于下半身脚部速度的局部极小值检测）距离过远，则给予负奖励。
- **半身一致性奖励**：基于上下半身法线方向的夹角计算，防止上下半身动作不同步。

最终损失为交叉熵损失与演员-评论家损失的加权组合。消融实验表明，去除演员-评论家微调后，Beat Align Score 从 0.2720 降至 0.2264（↓17%），FIDk 上升 3.23（15%），验证了 RL 微调对节拍对齐和运动质量的双重贡献。

### 补充图表

![[assets/figures/papers/2023_Bailando_3D_Dance_Generation_by_Actor_Critic_GPT_with_Choreographic_Memory_cdf67d1d7f60/figures/001_Figure_1.jpg]]
*Figure 1: Dance examples generated by our proposed method on various types of music. The character is from Mixamo [1]*

![[assets/figures/papers/2023_Bailando_3D_Dance_Generation_by_Actor_Critic_GPT_with_Choreographic_Memory_cdf67d1d7f60/figures/004_Figure_4.jpg]]
*Figure 4: Structure of 3D Pose VQ-VAE. The proposed 3D pose VQ-VAE is learned to encode and summarize meaningful dancing units to choreographic memory, and to reconstruct the target pose sequence from quantized features. The parameters of encoder and decoders and the codebook are jointly learned during training*

![[assets/figures/papers/2023_Bailando_3D_Dance_Generation_by_Actor_Critic_GPT_with_Choreographic_Memory_cdf67d1d7f60/figures/010_Figure_9.jpg]]
*Figure 9: The distribution of Bailando++ wins on different music types compared to the state of the arts. Each bar indicates the percentage that our method wins in comparison to the corresponding method*

![[assets/figures/papers/2023_Bailando_3D_Dance_Generation_by_Actor_Critic_GPT_with_Choreographic_Memory_cdf67d1d7f60/figures/014_Figure_11.jpg]]
*Figure 11: Interpretability of choreographic memory code. The sequence of a single code is decoded to a static pose, while the sequence of two various codes is decoded to a smooth transition between two poses, which means each code represents a dancing-style pose and the decoder links poses of different codes to movements*



## 实验与关键发现

### 主要定量结果

Bailando++ 在 AIST++ 测试集上进行了系统评估，与 **FACT** (Li et al., ICCV 2021)、**DanceFormer** (Li et al., AAAI 2022)、**EDGE** (Tseng et al., CVPR 2023) 以及前身版本 **Bailando** (Siyao et al., CVPR 2022 oral) 等基线方法进行了全面对比。评估指标涵盖运动质量（FIDk、FIDg）、运动多样性（Divk、Divg）和节拍对齐分数（Beat Align Score），同时辅以用户主观研究。

如表 I 所示，Bailando++ 在所有关键指标上均取得了最优性能：

- **运动质量**：FIDk 达到 **17.59**，相比 FACT 的 35.35 降低了 50.3%；FIDg 达到 **10.10**，相比 FACT 的 22.11 降低了 54.3%。这表明生成舞蹈的动力学特征分布与真实舞蹈高度一致。
- **运动多样性**：Divk 和 Divg 分别为 8.82 和 6.64，在保持高质量的同时维持了丰富的动作变化。
- **节拍对齐**：Beat Align Score 达到 **0.2720**，显著优于其他方法，验证了演员-评论家微调策略在同步音乐节拍方面的有效性。
- **用户研究**：Bailando++ 在所有对比方法上至少获得 **88.5%** 的胜率，在与 Bailando (CVPR 2022) 的直接对比中胜率达到 **78.0%**。图 9 展示了不同音乐类型（如芭蕾、嘻哈、街舞等）上的胜率分布，Bailando++ 在各风格上均保持显著优势。

值得注意的是，EDGE 在 FID 指标上表现较差但用户偏好较高，这提示 FID 指标可能无法完全反映人类主观偏好，需结合主观评估进行综合判断。

### 消融实验分析

为验证各模块的独立贡献，论文在 3D 关节位置域和 3D 关节旋转域分别进行了系统性消融实验（表 V 和表 VI），揭示了以下关键发现：

**编排记忆（量化）的核心作用**：去除 VQ-VAE 的量化机制（w/o. quantization）后，FIDg 从 10.10 急剧恶化至 **145.51**（↑135.41），运动质量几乎完全崩溃。这有力证明了离散码本约束对于保证生成姿态空间质量是不可或缺的——连续回归缺乏对姿态分布的有效约束，导致生成结果偏离真实舞蹈流形。

**跨条件因果注意力的协调机制**：去除跨条件因果注意力（w/o. cross-cond. att.）后，FIDk 上升 8.66（30%）至 26.32，FIDg 上升 3.70（31%）。该消融揭示了上下半身与音乐之间的交叉条件建模对于维持身体协调性和整体运动质量至关重要——独立的因果注意力无法有效捕捉跨组件依赖关系。

**混合训练策略的决定性影响**：在旋转域生成中，未使用混合训练策略（w/o. hybrid training）时，FIDk 从 17.59 飙升至 **39.09**（↑122%），且模型完全无法完成复杂转身动作。图 10 的可视化清晰展示了这一现象：在“foettes on pointe”（原地旋转）动作上，无混合训练的模型只能笨拙踢腿而无法转身。这证实了先在位置域学习空间结构、再迁移至旋转域的两阶段策略是旋转域生成成功的关键——直接优化旋转角度因距离度量与空间姿态差异不匹配而失败。

**上下文音乐编码的增强效果**：去除上下文音乐编码模块（w/o. CME）后，FIDk 上升 10.70（60%）至 28.29，FIDg 上升 2.61（26%）。这表明通过滑动窗口注意力增强音乐特征的长程依赖建模，对于提升舞蹈生成的时序连贯性具有显著贡献。

**演员-评论家微调的节拍对齐增益**：去除演员-评论家微调（w/o. actor-critic）后，Beat Align Score 从 0.2720 降至 0.2264（↓17%），FIDk 上升 3.23（15%）。这验证了基于节拍对齐奖励和身体一致性奖励的强化学习微调，能够在不显著损害运动质量的前提下有效提升音乐-动作同步性。

### VQ-VAE 模块消融

表 II 和表 IV 分别展示了在 3D 位置域和旋转域下 VQ-VAE 各子模块的贡献。速度-加速度损失项（velocity and acceleration loss items）在抑制生成舞蹈的抖动方面发挥了关键作用。表 III 进一步探究了下采样率 d 的影响，表明适当的时间下采样对于平衡码本表达能力与计算效率至关重要。

### 编排记忆的可解释性

图 11 直观展示了编排记忆码的可解释性：单个码解码为静态姿态，两个不同码的序列解码为姿态间的平滑过渡。这表明每个码代表一种具有舞蹈风格含义的姿态单元，解码器将不同姿态码链接为连续动作——编排记忆确实学习到了有意义的舞蹈基元。

### 失败模式与局限性

尽管 Bailando++ 在 AIST++ 上取得了优异性能，论文指出了以下局限性：

1. **领域差距**：模型在 AIST++ 数据集（主要为录音室音乐）上训练，迁移到“野外”任意风格音乐时存在性能退化，需要进一步在线策略微调。
2. **评估体系不足**：FID 等定量指标与人类主观偏好存在不一致（如 EDGE 的案例所示），当前评估体系尚不能完全捕捉舞蹈生成的美学质量。

### 关键图表索引

- **Table I**：AIST++ 测试集主要定量结果（运动质量、多样性、节拍对齐、用户研究）
- **Table V/VI**：Motion GPT 模块消融研究（位置域/旋转域），揭示量化、跨条件注意力、CME、演员-评论家等模块的贡献
- **Table II/IV**：Pose VQ-VAE 模块消融研究（位置域/旋转域）
- **Fig. 9**：不同音乐类型上用户研究胜率分布
- **Fig. 10**：混合训练策略在旋转域的有效性可视化（“foettes on pointe”动作）
- **Fig. 11**：编排记忆码的可解释性可视化（静态姿态与过渡）

![[assets/figures/papers/2023_Bailando_3D_Dance_Generation_by_Actor_Critic_GPT_with_Choreographic_Memory_cdf67d1d7f60/figures/013_Table.jpg]]
*Table: ABLATION STUDY ON DOWNSAMPLING RATE (d) IN POSE VQ-VAE (3D JOINT POSITION) TABLE IV ABLATION STUDY ON POSE VQ-VAE (3D JOINT ROTATION) TABLE V ABLATION STUDY ON MOTION GPT (3D JOINT POSITION). TABLE VI ABLATION STUDY ON MOTION GPT (3D JOINT ROTATION)*

![[assets/figures/papers/2023_Bailando_3D_Dance_Generation_by_Actor_Critic_GPT_with_Choreographic_Memory_cdf67d1d7f60/figures/011_Figure_10.jpg]]
*Figure 10: Visualization on the effectiveness of hybrid training. Here we show the dance generation result of “foettes on pointe” (spinning in place) with and without the hybrid training strategy when trained on the 3D joint rotation data. If learned without the hybrid training, the agent can only kick awkwardly and cannot turn around. The red lines indicate the orientations of the agent*

### 补充图表

![[assets/figures/papers/2023_Bailando_3D_Dance_Generation_by_Actor_Critic_GPT_with_Choreographic_Memory_cdf67d1d7f60/figures/015_Figure.jpg]]

![[assets/figures/papers/2023_Bailando_3D_Dance_Generation_by_Actor_Critic_GPT_with_Choreographic_Memory_cdf67d1d7f60/figures/003_Figure_3.jpg]]
*Figure 3: Comparison between Bailando and Bailando++. Here we present two examples where the avatar (a) kneels and (b) turn around. Errors that disobey the human morphology occur in avatar animation of the original Bailando (blue and red box). The inverse kinematics that transfer the 3D positions to 3D joint rotations of the original Bailando is conducted under the computer graphics software Unity*

![[assets/figures/papers/2023_Bailando_3D_Dance_Generation_by_Actor_Critic_GPT_with_Choreographic_Memory_cdf67d1d7f60/figures/007_Figure_7.jpg]]
*Figure 7: Contextual Music Encoding. In this encoding pipeline, music features in 60 fps with a length of T + 2 w are sampled and fed into a cascade of Transformer layers. The attention of the Transformer layer here aggregates adjacent music features within a ( 2 w + 1 ) )-wide sliding window. The augmented features are finally downsampled by an unshuffling operation [44] across the temporal dimension*



## 定位与知识库关联

### 1. 核心瓶颈与因果机制

Bailando++ 试图解决舞蹈生成领域的两个根本性瓶颈：**姿态空间的连续性与无约束性**，以及**音乐节拍与运动节奏的时间对齐困难**。现有方法（如 FACT、DanceFormer）通常直接从音乐特征回归连续的 3D 关节位置，这一映射缺乏对姿态质量的显式约束，容易产生违反人体形态的扭曲动作；同时，它们缺乏显式的节拍对齐机制，导致生成舞蹈与音乐节奏脱节。

Bailando++ 的核心因果调控旋钮是**离散量化的编排记忆**（Choreographic Memory）。通过 VQ-VAE 将连续姿态空间压缩为有限离散码本，模型在推理时从码本中“选择”姿态而非“回归”姿态，从而天然约束了生成姿态的质量边界。在此基础上，**演员-评论家强化学习微调**通过节拍对齐奖励函数，显式地将运动节奏与音乐节拍耦合。核心洞察可概括为：将舞蹈生成分解为“从音乐和过去姿态中自回归预测上下半身分离的离散姿态代码”，并借助跨条件因果注意力保持身体协调性，最终通过混合训练策略将输出域从 3D 位置升级为可直接驱动虚拟人的 SMPL 关节旋转角度。

### 2. 与基线方法的谱系关系

Bailando++ 处于“音乐驱动的 3D 舞蹈生成”这一任务线上，其直接前身是 **Bailando**（Siyao et al., CVPR 2022 Oral），后者首次引入了 VQ-VAE 码本和 GPT 自回归生成框架，但存在两个关键局限：(1) 输出为 3D 关节位置，需经逆运动学（IK）转换为旋转角才能驱动虚拟人，IK 过程引入不可微误差和形态失真；(2) 缺乏混合训练策略，无法直接在旋转域训练。

与此前基于 Transformer 的 **FACT**（Li et al., ICCV 2021）和 **DanceFormer**（Li et al., AAAI 2022）相比，Bailando++ 的差异化在于：
- **输出表示**：FACT 和 DanceFormer 输出 3D 位置或预裁剪动作片段，Bailando++ 输出 SMPL 旋转角，避免了 IK 后处理；
- **姿态空间建模**：基线方法在连续空间回归，Bailando++ 通过离散码本约束姿态质量——消融实验表明，去除量化后 FIDg 从 10.10 飙升至 145.51（↑135.41），充分说明码本对空间质量的保障是决定性的；
- **音乐编码**：Bailando++ 引入上下文音乐编码器（CME），通过滑动窗口 Transformer 增强音乐特征的长程依赖，去除 CME 导致 FIDk 上升 10.70（60%）；
- **节拍对齐**：基线方法无显式节拍约束，Bailando++ 通过演员-评论家微调将 Beat Align Score 从 0.2264 提升至 0.2720（↑20%）。

与基于扩散模型的 **EDGE**（Tseng et al., CVPR 2023）相比，Bailando++ 在 FID 指标上显著领先（FIDk 17.59 vs. EDGE 的 42+），但论文也坦承 FID 无法完全反映人类主观偏好——EDGE 在用户研究中表现较好，提示扩散模型可能生成更“自然”但 FID 距离较大的动作。这暴露了当前评估体系的局限性。

### 3. 适用边界与局限

Bailando++ 的适用边界受以下因素制约：

- **训练数据分布**：所有实验在 AIST++ 数据集上进行，该数据集包含 10 种舞蹈风格、严格对齐的录音室音乐。迁移到“野外”音乐（如流行歌曲、用户自拍视频配乐）时存在领域差距，论文明确指出需要进一步在线策略微调。
- **姿态码本的表达能力**：VQ-VAE 码本大小 $N$ 和下采样率 $d$ 是超参数，过小的码本会限制舞蹈多样性，过大的码本增加训练难度。消融实验（Table III）表明 $d=4$ 时取得最佳平衡，但该设置在更复杂的舞蹈动作（如街舞 Breaking）上是否足够尚需验证。
- **旋转域训练的代价**：混合训练策略是旋转域生成的必要条件——未使用混合训练时 FIDk 从 17.59 升至 39.09（↑122%），且无法完成转身动作（Fig. 10）。这一策略需要先在位置域预训练再微调解码器，增加了训练流程的复杂度。
- **评估指标的不完备性**：FID 指标与人类主观判断存在偏差，Beat Align Score 仅衡量节拍点的对齐而忽略了舞蹈编排的整体音乐性。用户研究虽能补充，但成本高昂且难以标准化。

### 4. 开放问题

1. **跨域泛化**：如何桥接从录音室音乐到任意风格音乐的领域差距？论文建议融入预训练的鲁棒音乐编码器（如 Jukebox），但这一方向尚未在本文中验证。

2. **评估体系设计**：如何构建更全面的舞蹈生成评估体系，将 FID 等空间质量指标、节拍对齐等时间一致性指标、以及人类主观偏好统一在一个框架下？多模态大模型（如 Video-LLaMA）是否可作为自动化的“虚拟评委”？

3. **长期舞蹈编排**：当前方法自回归预测下一帧姿态码，长期生成可能累积误差并导致舞蹈内容循环或退化。如何引入高层编排结构（如“引子-高潮-尾声”）来指导长期生成？

4. **交互式舞蹈生成**：演员-评论家框架天然支持在线策略优化，这是否意味着 Bailando++ 可以扩展到实时人机共舞场景，根据用户动作动态调整生成策略？



## 原文 PDF

![[paperPDFs/TPAMI_2023/Bailando_3D_Dance_Generation_by_Actor_Critic_GPT_with_Choreographic_Memory.pdf]]

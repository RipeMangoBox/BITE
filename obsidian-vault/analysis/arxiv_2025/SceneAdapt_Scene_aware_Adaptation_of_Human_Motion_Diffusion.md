---
title: "SceneAdapt: Scene-aware Adaptation of Human Motion Diffusion"
type: paper
paper_level: A
venue: arXiv
year: 2025
pdf_ref: paperPDFs/arxiv_2025/SceneAdapt_Scene_aware_Adaptation_of_Human_Motion_Diffusion.pdf
project_link: https://sceneadapt.github.io
aliases:
- SceneAdapt
tags:
- arxiv_2025
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
core_operator: 利用运动插值（motion inbetweening）作为代理任务，通过两阶段自适应将场景几何约束注入预训练文本-动作扩散模型，而无需三元组数据。第一阶段通过CaKey层使模型学习插值，第二阶段通过SceneCo层利用场景-动作对学习场景感知插值，从而在推理时实现文本驱动的场景感知运动生成。
primary_logic: 通过将场景感知建模为插值任务中的附加条件，可以桥接分离的数据集（文本-动作和场景-动作），在不损害原始语义生成能力的前提下将场景几何信息注入扩散模型，实现语义丰富且场景一致的运动生成。
claims:
- "SceneAdapt在场景感知文本生成中，相比MDM基线，大幅降低碰撞指标（CFR: 0.256 vs 0.316, MMP: 0.208 vs 0.319）同时保持文本对齐（RP@3: 0.792 vs 0.798）。"
- 移除阶段1（插值适应）直接训练场景感知模型导致FID显著上升（7.08 vs 0.497），RP下降，证明插值适应是保留文本-动作能力的关键。
- CaKey层的稀疏调制设计是插值性能的关键，替换为全局调制导致FID从0.036飙升至17.44。
- 增加阶段2的关键帧步长可提高场景感知，说明更稀疏的关键帧强制模型利用场景信息。
---

# SceneAdapt: Scene-aware Adaptation of Human Motion Diffusion

> [!tip] 核心洞察
> 通过将场景感知建模为插值任务中的附加条件，可以桥接分离的数据集（文本-动作和场景-动作），在不损害原始语义生成能力的前提下将场景几何信息注入扩散模型，实现语义丰富且场景一致的运动生成。

| 字段 | 内容 |
|------|------|
| 中文题名 | SceneAdapt：场景感知的人体运动扩散自适应 |
| 英文题名 | SceneAdapt: Scene-aware Adaptation of Human Motion Diffusion |
| 会议/期刊 | arXiv 2025 |
| Links | [arXiv](https://arxiv.org/abs/1907.01108) · [paper](https://arxiv.org/abs/2510.13044) · [Project](https://sceneadapt.github.io) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video |
| Method | SceneAdapt |
| Dataset | 自定义评估集（HML3D+TRUMANS合成）, HML3D测试集（插值） |

> [!tip] 效果简介
> - 自定义评估集（HML3D+TRUMANS合成） 上，RP@3↑ 0.792 (Ours ws=0.3) vs 0.798 (MDM) (-0.006)。
> - 自定义评估集 上，FID↓ 0.497 (Ours ws=0.3) vs 0.479 (MDM) (+0.018)；CFR↓ 0.256 (Ours ws=0.3) vs 0.316 (MDM) (-0.060)；MMP↓ 0.208 (Ours ws=0.3) vs 0.319 (MDM) (-0.111)。
> - HML3D测试集（插值） 上，FID↓ 0.036 (Ours) vs 7.258 (MDM imputation) (-7.222)。

## 概述

### 问题背景与核心瓶颈

文本驱动的三维人体运动生成近年来取得显著进展，但现有模型普遍缺乏**场景感知能力**，导致生成的运动会穿透墙壁、桌椅等静态障碍物。这一瓶颈的根源在于数据分布的割裂（见 Fig. 1）：文本-动作数据集（如 HML3D）语义丰富但无场景信息，场景-动作数据集（如 TRUMANS）虽包含场景约束，但其动作语义多样性极为有限。直接收集大规模文本-场景-动作三元组数据在成本上不可行，因此核心挑战在于**如何在不依赖三元组数据的前提下，同时实现语义丰富性和场景一致性**。

### 核心方法与洞察

SceneAdapt 提出了一种**两阶段自适应框架**，通过将场景感知建模为运动插值任务中的附加条件，桥接分离的数据集。其核心洞察在于：运动插值天然要求模型理解关键帧之间的运动流形，而场景约束可被形式化为对插值路径的几何限制。具体而言：

- **阶段一**：在冻结的预训练文本-动作扩散模型（MDM）中插入 **CaKey 层**，仅用文本-动作数据训练其进行运动插值，使模型获得关键帧条件生成能力，同时完整保留原始文本-动作生成流形。
- **阶段二**：引入 **SceneCo 层**，利用场景-动作对训练模型进行场景感知插值。通过稀疏关键帧策略和先验保持损失，将场景几何信息注入模型，而不损害阶段一建立的语义生成能力。

推理时，通过**文本与场景的双重分类器自由引导**，模型可同时接收文本提示和场景体素输入，生成语义丰富且场景一致的运动。

### 方法定位

SceneAdapt 属于**基于扩散模型的场景感知运动生成方法**，但区别于现有工作的关键点在于：

- **无需三元组数据**：与 HUMANISE cVAE、AffordMotion 等方法直接依赖文本-场景-动作三元组不同，SceneAdapt 仅使用分离的文本-动作和场景-动作数据。
- **保留预训练能力**：与直接在 MDM 上添加场景条件模块（如 MDM+SceneCo Layer、MDM+ControlNet）导致文本对齐能力显著退化不同，SceneAdapt 通过插值代理任务和两阶段训练策略，几乎无损地保留了预训练模型的语义生成能力。
- **稀疏条件机制**：CaKey 层的稀疏调制设计（仅在关键帧索引上施加仿射变换）是实现高质量插值和场景适应的关键，与全局调制或 LoRA 等密集适应方法形成对比。

### 主要结果

在自定义评估集上，SceneAdapt 相比 MDM 基线显著降低碰撞指标（**CFR**: 0.256 vs. 0.316；**MMP**: 0.208 vs. 0.319），同时保持文本对齐能力（**RP@3**: 0.792 vs. 0.798）和运动质量（**FID**: 0.497 vs. 0.479），证实了框架在场景感知与语义保真度之间的有效平衡。消融实验进一步验证了插值适应阶段和稀疏调制设计的必要性：移除阶段一直接训练场景感知模型导致 FID 从 0.497 飙升至 7.08，RP 从 0.791 降至 0.598；将 CaKey 替换为全局调制则使插值 FID 从 0.036 升至 17.44。

## 背景与动机

### 问题背景：文本驱动的人体运动生成

文本驱动的人体运动生成旨在从自然语言描述中合成逼真的三维人体动作序列。近年来，基于扩散模型的方法在这一领域取得了显著进展，其中**MDM**（Motion Diffusion Model）等预训练文本-动作扩散模型能够从大规模文本-动作数据集（如HML3D）中学习到丰富的语义运动先验，生成语义多样且自然的人体运动。

然而，这些模型存在一个根本性缺陷：**完全缺乏场景感知能力**。由于训练数据仅包含文本-动作对，模型无法理解三维场景的几何约束，导致生成的运动会穿透障碍物、与场景发生碰撞，无法直接应用于需要场景交互的实际任务（如室内导航、人机交互）。

### 现有方法的困境：语义丰富性与场景一致性的两难

解决场景感知运动生成的一种直接思路是在包含场景信息的数据集上训练模型。然而，现有场景-动作数据集（如TRUMANS、HUMANISE）面临两个关键瓶颈：

**数据分布的语义狭窄性**。如Fig. 1(a)所示，通过PCA可视化HML3D与场景感知数据集的运动嵌入分布，可以观察到场景感知数据集的分布范围明显更窄。这表明这些数据集中的运动语义多样性远低于纯文本-动作数据集——场景感知数据集中的人体运动往往局限于行走、站立等简单动作，难以覆盖“跳舞”、“挥手防御”等复杂语义。

**三元组数据的不可获取性**。理想的训练数据应为文本-场景-动作三元组，但收集大规模三元组数据在现实中不可行：一方面，为每个场景标注多样化文本描述需要大量人工；另一方面，为每个文本-场景对采集真实人体运动数据成本极高。现有合成数据集（如HUMANISE）虽然提供了三元组，但其运动语义受限于合成模板的多样性。

这导致了两种模型的系统性缺陷（Fig. 1(b-c)）：
- 在HML3D上训练的模型能够遵循“双手举起防御”的文本指令，但生成的运动会穿透沙发（场景感知缺失）。
- 在场景感知数据集上训练的模型能够避免碰撞，但无法理解复杂文本语义，可能生成与文本无关的动作（语义能力退化）。

### 核心动机：桥接分离的数据集

上述困境的本质在于：**语义丰富性**与**场景一致性**分别由两类分离的数据集提供，而直接合并或联合训练无法解决分布不匹配问题。

SceneAdapt的核心动机正是利用这两类数据集的互补性——文本-动作数据集提供语义多样性，场景-动作数据集提供几何约束——通过一种无需三元组数据的自适应策略，将场景感知能力注入预训练的文本-动作扩散模型，从而在保持原始语义生成能力的前提下，实现场景一致的运动生成。

## 核心创新

SceneAdapt的核心创新在于**通过运动插值代理任务，将场景几何约束注入预训练的文本-动作扩散模型，从而绕开对大规模文本-场景-动作三元组数据的依赖**。这一策略直接回应了真实瓶颈：文本-动作数据集（如HML3D）语义丰富但缺乏场景感知，而场景-动作数据集（如TRUMANS）满足场景约束但语义多样性有限，且收集三元组数据不可行。

### 关键改变槽位

与预训练MDM基线相比，SceneAdapt在三个维度上做出了根本性改变：

**1. 场景条件注入方式：从无场景输入到体素交叉注意力**

基线MDM仅以文本为条件生成运动，完全不具备场景感知能力。SceneAdapt引入**SceneCo层**，通过交叉注意力机制将体素块特征注入运动潜变量：

$$h_{out} = \mathrm{ATT}(h W_Q, s W_K, s W_V)$$

其中运动潜变量 $h$ 作为查询，体素块嵌入 $s$ 作为键和值。场景由**Voxel ViT**编码器提取块级嵌入，相比全局类别嵌入能获得更好的场景感知指标（Table 4）。这一设计使模型能够关注人体附近的场景几何区域——交叉注意力可视化（Fig. 7）证实模型主要关注人体邻近的场景区域。

**2. 关键帧约束机制：从无关键帧调节到稀疏仿射调制**

基线MDM仅依赖文本条件生成完整序列，无法利用已知姿态信息。SceneAdapt提出**CaKey层**，其核心机制是稀疏仿射调制：

$$\mathrm{CaKey}(a, m, x, t) = (1 - m) \odot a + m \odot \hat{a}$$

其中 $\hat{a} = \gamma \odot a + \beta$，$\gamma = f_\theta(x, t, a)$ 和 $\beta = h_\phi(x, t, a)$ 由两个MLP网络从运动、时间步和自注意激活中预测。关键设计在于**仅调制关键帧索引对应位置**（由掩码 $m$ 控制），非关键帧保持原样。消融实验（Table 6）表明，若替换为全局调制，FID从0.036飙升至17.44，MJPE恶化十余倍，证明稀疏调制是插值性能的关键。

**3. 训练策略：从直接训练到两阶段自适应**

基线直接在文本-动作对上训练扩散模型。SceneAdapt采用**两阶段自适应策略**：

- **阶段1（插值适应）**：冻结基模型参数，仅训练CaKey层，使用运动插值目标使模型学会在给定关键帧条件下生成连贯运动。此阶段仅需运动序列数据。
- **阶段2（场景感知插值适应）**：冻结CaKey层，添加SceneCo层，使用场景-动作对训练场景感知插值，并结合**先验保持损失**和**文本掩码设计**防止遗忘原始文本-动作能力。

移除阶段1直接训练场景感知模型会导致文本-动作生成能力崩溃：FID从0.497升至7.08，RP从0.791降至0.598（Table 5），证明插值适应是保留文本-动作能力的关键。在阶段2采用更稀疏的关键帧步长可迫使模型更依赖场景信息，进一步提升场景感知性能（Table 3, Fig. 6a）。

### 推理时的双引导采样

推理时，SceneAdapt通过结合文本和场景两种分类器自由引导实现可控生成：

$$\hat{x}_0 = \mathcal{D}_\theta(x_t, t, \mathcal{Q}_{text}, \mathcal{Q}_{scene}) + w_t(\mathcal{D}_\theta(\cdots, \mathcal{T}, \mathcal{Q}_{scene}) - \mathcal{D}_\theta(\cdots, \mathcal{Q}_{text}, \mathcal{Q}_{scene})) + w_s(\mathcal{D}_\theta(\cdots, \mathcal{Q}_{text}, \mathcal{S}) - \mathcal{D}_\theta(\cdots, \mathcal{Q}_{text}, \mathcal{Q}_{scene}))$$

通过调整 $w_t$ 和 $w_s$ 可以分别控制文本语义保真度和场景一致性强度，实现两者之间的灵活权衡（Fig. 6）。

### 核心洞察总结

SceneAdapt的根本洞察在于：**将场景感知建模为插值任务中的附加条件，可以桥接分离的数据集（文本-动作和场景-动作），在不损害原始语义生成能力的前提下将场景几何信息注入扩散模型**。这一策略使得模型在场景感知文本生成中，相比MDM基线大幅降低碰撞指标（CFR: 0.256 vs 0.316, MMP: 0.208 vs 0.319），同时保持文本对齐（RP@3: 0.792 vs 0.798）（Table 1）。

## 整体框架

SceneAdapt 采用两阶段自适应策略，将场景几何约束注入预训练的文本-动作扩散模型（MDM），而无需昂贵的文本-场景-动作三元组数据。其核心思想是将场景感知建模为运动插值（motion inbetweening）任务中的附加条件，从而桥接语义丰富但无场景的文本-动作数据集与场景-动作数据集，在不损害原始文本-动作生成能力的前提下实现场景一致性运动生成。

### Pipeline 总览

整体流程分为三个阶段（见 Fig. 2）：

![[assets/figures/papers/paper_list_l1694_SceneAdapt_Scene_aware_Adaptation_of_Human_Motion_Diffusion/figures/002_Figure_2.jpg]]
*Figure 2: Overview. Starting from a pretrained text-to-motion model (Stage 0), we first insert CaKey layers and train them with a motion inbetweening objective (Stage 1), which only requires motion sequences. We then add scene-conditioning (SceneCo) layers and train them with a scene-aware inbetweening objective (Stage 2), using scene-motion pairs. During inference, we use the base model and adaptors to generate semantically rich motion which also adheres to the scene geometry*

1. **Stage 0 — 预训练基础模型**：使用大规模文本-动作对训练一个标准的文本条件运动扩散模型（MDM），该模型具备丰富的语义生成能力，但完全不感知场景几何。

2. **Stage 1 — 插值适应（Inbetweening Adaptation）**：在冻结的 MDM 中插入 CaKey 层（Context-aware Keyframing Layer），仅用运动序列数据训练插值能力。CaKey 层通过稀疏仿射调制，在给定关键帧的条件下生成完整运动序列，使模型学会在约束下进行运动补全。

3. **Stage 2 — 场景感知插值适应（Scene-aware Inbetweening Adaptation）**：在 Stage 1 的基础上，进一步添加 SceneCo 层（Scene-Conditioning Cross-Attention Layer）和体素场景编码器 Voxel ViT，使用场景-动作对进行训练。此时模型学习在场景几何约束下完成插值，从而获得场景感知能力。

推理时，通过双引导（dual-guidance）采样机制，同时接受文本条件和场景条件，生成语义丰富且场景一致的人体运动。

### 模块关系与数据流

**预训练 MDM** 作为整个框架的生成骨干，接受文本嵌入 $\mathcal{T}$ 作为条件，通过扩散去噪过程从噪声 $x_t$ 恢复运动序列 $x_0$。其训练目标为简化的 L2 重建损失：

$$\mathcal{L}_{\mathrm{t2m}} = \mathbb{E}_{{x_0} \sim q({x_0} \mid T), t \sim [1, T]} \left[ \| {x_0} - {\mathcal{D}_\theta({x_t}, t, \mathcal{T})} \|_2^2 \right]$$

**CaKey 层**插入在 MDM 的 Transformer 层中，负责关键帧约束调制。给定关键帧掩码 $m$（在关键帧索引处为 1，其余为 0），CaKey 层通过两个 MLP 网络 $f_\theta$ 和 $h_\phi$ 从运动潜变量 $x$、时间步 $t$ 和自注意力激活 $a$ 中预测缩放参数 $\gamma$ 和平移参数 $\beta$：

$$\gamma = f_\theta(x, t, a), \quad \beta = h_\phi(x, t, a)$$

然后对激活进行仿射变换 $\widehat{a} = \gamma \odot a + \beta$，并通过稀疏调制仅在关键帧位置应用：

$$\mathrm{CaKey}(a, m, x, t) = (1 - m) \odot a + m \odot \widehat{a}$$

这一设计使得关键帧约束以稀疏方式注入，非关键帧保持原始运动流形的完整性，是插值性能的关键。

**SceneCo 层**以交叉注意力机制将场景信息注入运动潜变量。场景首先由 Voxel ViT 编码为体素块嵌入 $s$，随后运动潜变量 $h$ 作为查询（Query），体素块嵌入作为键（Key）和值（Value）进行交叉注意力计算：

$$h_{out} = \mathrm{ATT}(h W_Q, s W_K, s W_V)$$

这种块级场景表示使模型能够关注人体周围的局部几何结构，而非全局场景类别标签。

**双引导采样**在推理时结合文本和场景两种分类器自由引导（CFG），通过权重 $w_t$ 和 $w_s$ 分别控制文本和场景条件的影响强度：

$$\hat{x}_0 = \mathcal{D}_\theta(x_t, t, \mathcal{Q}_{text}, \mathcal{Q}_{scene}) + w_t(\mathcal{D}_\theta(\cdots, \mathcal{T}, \mathcal{Q}_{scene}) - \mathcal{D}_\theta(\cdots, \mathcal{Q}_{text}, \mathcal{Q}_{scene})) + w_s(\mathcal{D}_\theta(\cdots, \mathcal{Q}_{text}, \mathcal{S}) - \mathcal{D}_\theta(\cdots, \mathcal{Q}_{text}, \mathcal{Q}_{scene}))$$

### 训练策略

Stage 1 的训练完全冻结 MDM 参数，仅优化 CaKey 层。训练数据为纯运动序列，关键帧步长设为 20（约每秒一个关键帧），使模型学会在稀疏关键帧约束下生成连贯运动。

Stage 2 的训练冻结 CaKey 层，仅优化 SceneCo 层和 Voxel ViT。此时使用场景-动作对，并采用更稀疏的关键帧（更大步长）以迫使模型主动利用场景几何信息完成插值。同时引入先验保持损失（prior preserving loss）和文本掩码设计，防止场景适应过程破坏 Stage 1 获得的文本-动作生成能力。

### 输入输出流

- **训练输入**：Stage 1 接受运动序列及关键帧掩码；Stage 2 接受场景体素、运动序列及关键帧掩码。
- **推理输入**：文本描述、3D 场景体素，可选的目标姿态（作为极端稀疏的关键帧）。
- **输出**：与场景几何一致且语义对齐文本的完整人体运动序列。

## 核心模块与公式推导

SceneAdapt 的核心架构由四个关键模块构成，它们以两阶段自适应的方式协同工作，将场景几何约束注入预训练的文本-动作扩散模型。

### 预训练文本-动作扩散模型（Stage 0）

基础模型采用 **MDM**（Motion Diffusion Model），这是一个以文本为条件的运动扩散模型。其训练目标为简化的 L2 重建损失：

$$\mathcal{L}_{\mathrm{t2m}} = \mathbb{E}_{{x_0} \sim q({x_0} \mid T), t \sim [1, T]} \left[ \| {x_0} - {\mathcal{D}_\theta({x_t}, t, \mathcal{T})} \|_2^2 \right] \tag{1}$$

其中 $x_0$ 为真实运动序列，$\mathcal{T}$ 为文本嵌入，$\mathcal{D}_\theta$ 为去噪网络，$t$ 为扩散时间步。该模型在 HML3D 等大规模文本-动作数据集上预训练，具备丰富的语义生成能力，但完全缺乏场景感知。

### CaKey 层：上下文感知关键帧调制（Stage 1）

CaKey（Context-aware Keyframing）层是整个框架的**核心创新**，其设计目标是使预训练 MDM 具备运动插值能力，同时不破坏原始文本-动作生成流形。

**调制参数生成**：CaKey 通过两个可学习的 MLP 网络 $f_\theta$ 和 $h_\phi$，从运动潜变量 $x$、扩散时间步 $t$ 以及自注意力激活 $a$ 中预测缩放参数 $\gamma$ 和平移参数 $\beta$：

$$\gamma = f_\theta(x, t, a), \quad \beta = h_\phi(x, t, a) \tag{2}$$

随后对激活进行仿射调制：

$$\widehat{a} = \gamma \odot a + \beta \tag{3}$$

**稀疏调制机制**：CaKey 的关键设计在于**仅在关键帧索引上施加调制**，非关键帧保持原始激活不变。设关键帧掩码为 $m$（关键帧位置为 1，其余为 0），则最终输出为：

$$\mathrm{CaKey}(a, m, x, t) = (1 - m) \odot a + m \odot \hat{a} \tag{4}$$

这一稀疏调制设计具有双重优势：（1）关键帧位置获得上下文感知的条件信号，实现精确插值；（2）非关键帧完全保留预训练模型的原始行为，避免对文本-动作生成能力的破坏。消融实验证实，若将稀疏调制替换为全局调制，FID 从 0.036 飙升至 17.44（Table 6），充分验证了稀疏设计的必要性。

**Stage 1 训练**：冻结 MDM 基座参数，仅优化 CaKey 层，使用运动插值目标进行训练。关键帧步长设为 20（约每秒一个关键帧）。

### SceneCo 层与 Voxel ViT：场景条件注入（Stage 2）

SceneCo（Scene Conditioning）层负责将场景几何信息注入运动潜变量。场景首先通过 **Voxel ViT** 编码器处理：将场景体素化为固定分辨率的三维网格，再由 Vision Transformer 提取块级（patch）场景嵌入 $s$。

SceneCo 层采用交叉注意力机制，以运动潜变量 $h$ 作为查询（Query），体素块嵌入 $s$ 作为键（Key）和值（Value）：

$$h_{out} = \mathrm{ATT}(h W_Q, s W_K, s W_V) \tag{5}$$

消融实验表明，块级场景嵌入优于全局类别嵌入（Table 4），因为前者保留了空间局部性，使模型能够关注人体附近的场景区域。交叉注意力可视化（Fig. 7）证实模型主要关注人体邻近的场景几何。

![[assets/figures/papers/paper_list_l1694_SceneAdapt_Scene_aware_Adaptation_of_Human_Motion_Diffusion/figures/011_Figure_7.jpg]]
*Figure 7: Visualization of cross-attention weight maps between the motion latent at a given timestep and patch-wise scene embeddings. The red point marks the human location. As highlighted by the blue boxes, the model predominantly attends to scene regions in the human’s immediate vicinity*

**Stage 2 训练**：冻结 CaKey 层，仅训练 SceneCo 层和 Voxel ViT，使用场景-动作对进行场景感知插值训练。训练时引入先验保持损失和文本掩码，以防止场景适应破坏原始文本-动作能力（Fig. 6b）。

### 双引导采样

推理阶段采用分类器自由引导（Classifier-Free Guidance），同时平衡文本条件和场景条件的影响。最终采样公式为：

$$\hat{x}_0 = \mathcal{D}_\theta(x_t, t, \mathcal{Q}_{text}, \mathcal{Q}_{scene}) + w_t(\mathcal{D}_\theta(\cdots, \mathcal{T}, \mathcal{Q}_{scene}) - \mathcal{D}_\theta(\cdots, \mathcal{Q}_{text}, \mathcal{Q}_{scene})) + w_s(\mathcal{D}_\theta(\cdots, \mathcal{Q}_{text}, \mathcal{S}) - \mathcal{D}_\theta(\cdots, \mathcal{Q}_{text}, \mathcal{Q}_{scene})) \tag{6}$$

其中 $w_t$ 控制文本引导强度，$w_s$ 控制场景引导强度，$\mathcal{Q}_{text}$ 和 $\mathcal{Q}_{scene}$ 分别为空文本和空场景嵌入。通过调节 $w_s$，用户可在文本语义保真度与场景一致性之间进行灵活权衡。

### 辅助损失函数

为提升生成运动的自然度，训练阶段额外引入两个辅助损失。关节位置损失通过正向运动学（FK）计算关节位置的 L2 重建误差：

$$\mathcal{L}_{\mathrm{joints}} = \mathbb{E}_{\boldsymbol{x}_0 \sim \boldsymbol{q}(\boldsymbol{x}_0 | \mathcal{T}), t \sim [1, T]} \Big[ \big\| \mathrm{FK}(\boldsymbol{x}_0) - \mathrm{FK}(\mathcal{D}_{\theta}(\boldsymbol{x}_t, t, \mathcal{T})) \big\|_2^2 \Big] \tag{7}$$

速度损失则约束关节位置的时间差分，抑制滑步等伪影：

$$\mathcal{L}_{\mathrm{vel}} = \mathbb{E}_{x_0 \sim q(x_0 | T), t \sim [1, T]} \left[ \left| \left| \mathrm{diff}(\mathrm{FK}(x_0)) - \mathrm{diff}(\mathrm{FK}(\mathcal{D}_{\theta}(x_t, t, T))) \right| \right|_2^2 \right] \tag{8}$$

总损失为三者的加权组合：

$$\mathcal{L} = \mathcal{L}_{\mathrm{t2m}} + \lambda_{\mathrm{joints}} \mathcal{L}_{\mathrm{joints}} + \lambda_{\mathrm{vel}} \mathcal{L}_{\mathrm{vel}} \tag{9}$$

其中权重设置为 $\lambda_{\mathrm{joints}}=1$，$\lambda_{\mathrm{vel}}=100$。

## 实验与分析

### 主结果：场景感知文本驱动运动生成

SceneAdapt 的核心目标是保持预训练文本-动作模型的语义丰富性，同时注入场景几何约束。Table 1 展示了在自定义评估集上的定量对比。该评估集通过组合 HML3D 动作与 TRUMANS 场景构建，并筛除需要特殊地形（如楼梯）的文本以保证物理合理性。

![[assets/figures/papers/paper_list_l1694_SceneAdapt_Scene_aware_Adaptation_of_Human_Motion_Diffusion/figures/004_Table_1.jpg]]
*Table 1: Scene-aware text-driven generation results on our evaluation set. T–M indicates training with text–motion pairs (e.g., HML3D), T–S–M indicates text– scene–motion triplets (e.g., HUMANISE), and S–M indicates scene–motion pairs (e.g., TRUMANS). “Inf. Time” reports the average inference time per sample in RTX A5000*

**关键发现：SceneAdapt 在几乎不损失文本对齐能力的前提下，显著降低了碰撞指标。** 以 $w_s=0.3$ 的配置为例：

- **文本对齐保持**：RP@3 为 0.792，与 MDM 基线的 0.798 几乎持平（仅下降 0.006），证明两阶段自适应策略有效保护了原始语义生成能力。
- **场景一致性大幅提升**：碰撞帧率 CFR 从 MDM 的 0.316 降至 0.256（下降 19%），最小穿透距离 MMP 从 0.319 降至 0.208（下降 35%），关节碰撞率 JCR 从 0.344 降至 0.246（下降 28%）。
- **运动质量保持**：FID 仅从 0.479 微升至 0.497，表明生成运动的整体分布未受破坏。

与直接训练场景感知模型的方法对比，优势更为突出。**HUMANISE cVAE** 虽使用文本-场景-动作三元组数据训练，但其 RP@3 仅为 0.417，语义多样性严重受限——这直接验证了本文的核心动机：场景-动作数据集的语义覆盖远窄于纯文本-动作数据集（Fig. 1a）。**AffordMotion** 和 **DNO** 在场景指标上有所改善，但文本对齐能力明显弱于 SceneAdapt。MDM+ControlNet 和 MDM+SceneCo Layer 等直接插入场景条件模块的基线，同样出现文本对齐退化，说明简单的条件注入会扰乱预训练运动流形。

定性结果（Fig. 4）进一步印证了这一结论：AffordMotion 存在场景穿透，DNO 文本对齐较弱，而 SceneAdapt 在增强场景感知的同时保持了文本忠实度。

![[assets/figures/papers/paper_list_l1694_SceneAdapt_Scene_aware_Adaptation_of_Human_Motion_Diffusion/figures/005_Figure_4.jpg]]
*Figure 4: Qualitative results. Boxes mark collisions and Xs mark semantic errors. Unlike AffordMotion (scene penetration) and DNO (weak text alignment), our method improves MDM by enhancing scene-awareness while preserving text fidelity*

### 运动插值能力验证

阶段1的插值适应是 SceneAdapt 成功的基础。Table 2 展示了在 HML3D 测试集上的运动插值结果：

![[assets/figures/papers/paper_list_l1694_SceneAdapt_Scene_aware_Adaptation_of_Human_Motion_Diffusion/figures/006_Table_2.jpg]]
*Table 2: Motion inbetweening results on the HML3D test set. Our CaKey design outperforms imputation sampling, LoRA, and CondMDI, highlighting the importance of context-aware modulation. Extensive ablations provided in Suppl.§ 2*

- **CaKey 的绝对优势**：SceneAdapt 的 FID 仅为 0.036，而 MDM imputation sampling 为 7.258，LoRA 为 0.278，CondMDI 为 0.056。CaKey 在关键帧重建精度（MJPE(Key)=0.0018）和整体运动质量（MJPE(All)=0.0550）上均达到最优。
- **足部滑步抑制**：Foot skating 指标为 0.0479，滑步比率 0.0623，均优于所有基线，说明上下文感知调制能生成更自然的足部接触。

### 消融分析

#### 阶段1的必要性（Table 5）

![[assets/figures/papers/paper_list_l1694_SceneAdapt_Scene_aware_Adaptation_of_Human_Motion_Diffusion/figures/012_Table_5.jpg]]
*Table 5: Effect of stage 1*

移除阶段1直接训练场景感知插值会导致灾难性后果：
- **FID 从 0.497 飙升至 7.08**（恶化 14 倍），RP@3 从 0.791 降至 0.598。
- 这证明插值适应是保留文本-动作生成能力的关键——它使模型先学会在运动流形内进行条件生成，再引入场景约束，避免了直接微调对预训练权重的破坏。

#### CaKey 组件设计（Table 6）

![[assets/figures/papers/paper_list_l1694_SceneAdapt_Scene_aware_Adaptation_of_Human_Motion_Diffusion/figures/014_Table_6.jpg]]
*Table 6: Ablation study on motion inbetweening designs. Sparse Mod. indicates whether sparse modulation is used. Adaptive denotes whether the source latent is provided as input to the modulator. Time emb. specifies whether time embedding is provided as input to the modulator. Modulator describes how*

CaKey 的稀疏调制设计是其插值性能的核心：
- **移除稀疏调制**（全局调制）：FID 从 0.036 飙升至 17.44，MJPE(All) 恶化十余倍。这说明仅调制关键帧是保留非关键帧区域运动自然度的必要条件。
- **移除上下文感知**（不提供源潜变量）：FID 升至 0.112，MJPE(All) 升至 0.0722，性能明显退化。
- **移除时间嵌入**：FID 升至 0.089，MJPE(All) 升至 0.0701，表明时间步信息对调制精度有贡献。

#### 关键帧步长的影响（Table 3, Fig. 6a）

![[assets/figures/papers/paper_list_l1694_SceneAdapt_Scene_aware_Adaptation_of_Human_Motion_Diffusion/figures/008_Table_3.jpg]]
*Table 3: Scene-awareness results on TRUMANS for inbetweening. to more effectively exploit scene inparser keyframe settings*

阶段2训练时采用更稀疏的关键帧（更大步长）可迫使模型更依赖场景信息：
- 随着关键帧步长增加，场景感知指标（CFR、MMP）呈改善趋势。
- Fig. 6a 展示了不同步长下场景感知与文本对齐的权衡曲线：更稀疏的关键帧使模型在相同 $w_s$ 下获得更好的场景一致性，但极端稀疏可能损害插值精度。

#### 场景表示方式（Table 4）

![[assets/figures/papers/paper_list_l1694_SceneAdapt_Scene_aware_Adaptation_of_Human_Motion_Diffusion/figures/010_Table_4.jpg]]
*Table 4: Effect of Scene Rep*

**块级（patch）场景嵌入优于全局类别嵌入**：
- 使用 Voxel ViT 提取的块级特征在场景感知指标上全面优于全局池化表示。
- 交叉注意力可视化（Fig. 7）揭示了原因：模型主要关注人体附近的场景区域，块级表示能提供更精细的空间信息。

#### 先验保持设计（Fig. 6b）

阶段2训练中的先验保持损失和文本掩码对保留原始能力至关重要：
- Fig. 6b 展示了有无先验保持设计的对比曲线：引入先验损失和文本掩码后，在不同 $w_s$ 下均能获得更好的文本对齐-场景感知权衡。
- 这些设计防止了场景条件训练对文本-动作映射的灾难性遗忘。

### 穿透深度分布分析（Fig. 9, Table 7）

Fig. 9 展示了各方法在碰撞帧上的每帧最大穿透深度分布。SceneAdapt 不仅减少了碰撞帧数，还显著降低了穿透深度：大部分碰撞帧的穿透深度集中在较小值域，而 MDM 和 AffordMotion 的分布尾部更长。Table 7 的穿透统计进一步量化了这一优势，SceneAdapt 在平均穿透深度和最大穿透深度上均优于对比方法。

### 目标姿态条件扩展（Fig. 5）

![[assets/figures/papers/paper_list_l1694_SceneAdapt_Scene_aware_Adaptation_of_Human_Motion_Diffusion/figures/007_Figure_5.jpg]]
*Figure 5: Goal pose conditioned scene-aware text-to-motion generation. Interpreting the goal pose as an extremely sparse keyframe, SceneAdapt produces sceneconsistent motion conditioned on text, scene, and goal pose. Goal poses are in yellow*

将目标姿态视为极端稀疏的关键帧，SceneAdapt 可自然地扩展为目标姿态条件的场景感知生成。Fig. 5 展示了模型在给定目标姿态（黄色标记）时，能生成坐下、伸手等与场景几何一致的运动。这为功能性目标导向的运动生成提供了可行路径，尽管当前方法尚未显式建模场景语义关系。

### 失败模式与局限

1. **语义理解缺失**：模型无法理解“走向冰箱”这类功能性指令，需要额外的目标姿态或语义推理模块来指定空间目标。
2. **单人限制**：当前框架仅支持单人运动生成，未扩展到多人交互场景。
3. **手部缺失**：未建模手部关节，无法生成手部交互动作（如抓取物体）。
4. **静态场景假设**：场景表示为静态体素，无法处理动态场景或物体状态变化。
5. **数据依赖**：训练依赖于对 TRUMANS 数据的降采样，可能影响对不同运动速度的适应性。评估集通过筛选排除了楼梯等特殊地形，实际部署时可能遇到更复杂的几何约束。

### 方法谱系与知识库定位

SceneAdapt 处于**预训练模型自适应**与**场景感知运动生成**的交叉点：

- **运动扩散模型**：基于 **MDM** 的预训练文本-动作扩散框架，继承了其 Transformer 架构和分类器自由引导机制。
- **参数高效自适应**：CaKey 层的稀疏调制设计借鉴了 ControlNet 的条件注入思想，但通过关键帧掩码实现了更精细的控制，避免了 LoRA 等低秩自适应方法的性能退化（Table 2 中 LoRA 的 FID 为 0.278，远高于 CaKey 的 0.036）。
- **场景感知生成**：与 **AffordMotion**（利用场景几何和文本生成交互运动）、**DNO**（基于梯度引导的优化方法）、**HUMANISE cVAE**（合成数据训练）等方法相比，SceneAdapt 的核心差异在于**无需三元组数据**，通过解耦数据集和两阶段自适应实现场景感知注入。
- **运动插值**：CondMDI 等方法也探索了扩散模型的插值能力，但 CaKey 通过上下文感知的稀疏调制在精度和自然度上实现了显著提升。

### 补充图表

![[assets/figures/papers/paper_list_l1694_SceneAdapt_Scene_aware_Adaptation_of_Human_Motion_Diffusion/figures/009_Figure_6.jpg]]
*Figure 6: Ablation Studies. Each dot represents a certain*

![[assets/figures/papers/paper_list_l1694_SceneAdapt_Scene_aware_Adaptation_of_Human_Motion_Diffusion/figures/001_Figure_1.jpg]]
*Figure 1: Motivation. (a) Distribution of motion embeddings of HML3D [14] and sceneaware datasets [23, 49] visualized via PCA. Scene-aware datasets show narrower distributions than HML3D, indicating lower semantic coverage. (b) Models trained on HML3D capture diverse action semantics but lack scene-awareness, penetrating the obstacles. (c) Models trained on scene-aware datasets satisfy scene constraints, but fail to follow text prompts because the datasets contain limited semantic motion diversity*

## 方法谱系与知识库定位

### 核心问题定位

SceneAdapt 瞄准的是场景感知人体运动生成中的一个结构性数据瓶颈：**文本-动作模型**（如 **MDM**）在 HML3D 等大规模数据集上训练，语义覆盖广但完全缺乏场景意识，生成的运动会穿透障碍物；**场景-动作模型**（如 **AffordMotion**、**HUMANISE cVAE**）在 TRUMANS、HUMANISE 等场景-动作对上训练，能遵守场景约束，但这些数据集的运动语义多样性远低于 HML3D（Fig. 1 的 PCA 可视化明确展示了这一分布差异）。直接收集文本-场景-动作三元组数据在规模上不可行，因此现有方法被迫在“语义丰富性”和“场景一致性”之间做取舍。SceneAdapt 的核心洞察是：**运动插值（motion inbetweening）可以作为代理任务，桥接这两个分离的数据域**——插值只需要运动序列本身，而场景感知插值只需要场景-动作对，两者都不需要文本-场景-动作三元组。

### 与基线方法的关系

**MDM 及其直接扩展**。SceneAdapt 以 **MDM**（Motion Diffusion Model）为预训练基座，这是文本-动作扩散模型的代表性工作。直接对 MDM 添加场景条件有两种朴素策略：(1) **MDM+ControlNet**，在 MDM 中插入 ControlNet 风格的条件模块，但 ControlNet 的“零卷积”设计在扩散 Transformer 架构上缺乏验证，且需要大量场景-动作对从头训练；(2) **MDM+SceneCo Layer**，直接在 MDM 中插入场景条件交叉注意力层进行微调，这会导致灾难性遗忘——Table 5 显示，移除阶段1直接训练场景感知模型，FID 从 0.497 飙升至 7.08，RP@3 从 0.791 跌至 0.598。SceneAdapt 通过两阶段自适应策略避免了这一问题：阶段1先让模型学会插值（冻结基座，仅训练 CaKey 层），阶段2再在冻结插值模块的基础上学习场景感知插值，从而保留了原始文本-动作生成能力。

**场景-动作生成模型**。**AffordMotion** 利用场景几何和文本生成交互运动，但其训练数据（场景-动作对）的语义多样性有限，导致文本对齐能力弱（Table 1 中 RP@3 仅为 0.693，而 SceneAdapt 达到 0.792）。**HUMANISE cVAE** 基于合成文本-场景-动作三元组训练，虽然同时具备文本和场景条件，但合成数据的质量限制了其泛化性。SceneAdapt 的独特之处在于**从未见过三元组数据**，仅通过分离的数据集和两阶段自适应就实现了更好的综合性能。

**基于优化的方法**。**DNO** 采用梯度引导的方式在推理时优化运动以遵守场景约束，不需要场景-动作训练数据。但 DNO 的文本对齐能力弱（Table 1 中 RP@3 仅 0.717），且推理速度慢（Table 1 中推理时间 2.33s，而 SceneAdapt 仅需 0.07s）。SceneAdapt 将场景约束直接注入模型参数，推理时无需额外优化步骤。

**运动插值方法**。在纯插值任务上，SceneAdapt 的 CaKey 设计显著优于 MDM 的 imputation sampling（FID: 0.036 vs 7.258, Table 2），也优于 **LoRA** 和 **CondMDI** 等参数高效微调方法。关键在于 CaKey 的**稀疏调制**机制——仅在关键帧索引上应用仿射变换，非关键帧保持原样（Eq. 4）。Table 6 的消融显示，若替换为全局调制，FID 从 0.036 飙升至 17.44，MJPE 恶化十余倍，证明稀疏性是保留运动质量的关键。

**实时控制方法**。**DARTControl** 基于扩散自回归模型实现实时文本驱动运动控制，侧重于交互式应用场景。SceneAdapt 与之正交——DARTControl 解决的是控制精度和实时性问题，而 SceneAdapt 解决的是场景几何约束的注入问题。SceneAdapt 通过将目标姿态解释为极稀疏关键帧（Fig. 5），也展示了目标导向的场景感知生成能力，但未达到 DARTControl 的实时交互级别。

### 方法适用边界

**适用场景**：
- 文本驱动的场景感知运动生成，特别是需要同时保持语义丰富性和场景一致性的场景
- 运动插值任务（给定关键帧，生成中间帧），包括场景感知插值和纯运动插值
- 目标姿态条件下的场景感知生成（将目标姿态视为极稀疏关键帧）
- 静态场景下的单人运动生成

**不适用场景**：
- **场景语义理解**：SceneAdapt 无法直接建模“走向冰箱”这类功能性语义关系，因为场景编码器（Voxel ViT）提取的是几何体素特征而非语义对象标签。要实现功能性目标导向的运动，需要额外的目标姿态输入或语义推理模块。
- **多人交互**：当前框架仅支持单人运动生成，未扩展到多人场景。
- **手部交互**：运动表示未包含手部关节，无法生成抓取、推动等精细交互动作。
- **动态场景**：场景表示依赖静态体素，未处理物体状态变化或动态障碍物。

### 局限与开放问题

**已确认的局限**（来自论文自身声明和实验证据）：
1. **功能性语义缺失**：无法直接建模“走向冰箱并打开门”这类需要场景语义理解的指令，需要额外的高层规划模块。
2. **单人限制**：框架设计为单人运动，多人场景感知生成是完全开放的问题。
3. **手部缺失**：当前运动表示不包含手部关节，限制了交互动作的精细度。
4. **静态场景假设**：Voxel ViT 编码的是静态体素场景，无法适应动态变化的物体状态。
5. **运动速度偏差**：阶段2训练依赖于对 TRUMANS 数据的降采样（将 30fps 降为 20fps 以匹配 HML3D），可能影响对不同运动速度的适应性。

**开放研究问题**：
- **场景语义集成**：如何将场景语义理解（对象检测、功能可供性）融入框架，使模型能根据文本指令自主确定目标位置和行为类型？这可能需要结合视觉-语言模型或多模态场景表示。
- **全身模型扩展**：扩展到包含手部关节的全身模型（如 SMPL-X），以生成更精细的交互动作。这需要相应的高质量手部-场景交互数据集。
- **多人场景感知**：支持多人场景感知运动生成，涉及人与人、人与场景的复杂交互建模，是当前领域的主要开放挑战。
- **物理合理性增强**：虽然 SceneAdapt 通过碰撞指标（CFR, MMP）衡量物理约束，但未显式建模物理模拟。集成物理模拟或控制理论（如接触力约束、平衡控制）可进一步提升运动的物理合理性。
- **动态场景适应**：如何使模型适应动态变化的场景（如移动的家具、开关的门），可能需要时序场景表示或在线自适应机制。

### 方法定位总结

SceneAdapt 在场景感知运动生成领域占据了一个独特的方法论位置：它**不是**从头训练的场景感知模型，也**不是**纯推理时的优化方法，而是**基于预训练模型的两阶段自适应框架**。这种方法论介于“数据驱动训练”和“测试时优化”之间，通过插值代理任务实现了跨数据域的知识迁移。其核心贡献在于证明了：在无法获取三元组数据的情况下，通过精心设计的自适应策略（稀疏关键帧调制 + 场景条件交叉注意力 + 先验保持损失），可以将几何约束注入预训练语义模型，同时保留原始生成能力。这一思路对更广泛的“预训练模型领域自适应”问题具有启示意义——当目标域数据稀缺但存在与源域共享底层结构的代理任务时，分阶段自适应可能是比直接微调更有效的策略。

## 原文 PDF

![[paperPDFs/arxiv_2025/SceneAdapt_Scene_aware_Adaptation_of_Human_Motion_Diffusion.pdf]]
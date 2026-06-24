---
title: "ReGenNet: Towards Human Action-Reaction Synthesis"
type: paper
paper_level: A
venue: CVPR
year: 2024
pdf_ref: paperPDFs/CVPR_2024/ReGenNet_Towards_Human_Action_Reaction_Synthesis.pdf
aliases:
- ReGenNet
tags:
- CVPR_2024
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 通过显式标注行动者-反应者顺序，并采用基于Transformer解码器的条件扩散模型（防止未来信息泄漏）以及距离驱动的显式交互损失，使模型能够即时生成符合交互语义且身体细节丰富的反应。
primary_logic: 将人类交互分解为行动者与反应者的非对称关系，利用扩散模型预测干净姿势，并直接对相对姿态、方向和根位移施加L2交互损失，从而大幅提升反应生成的即时性和物理一致性。
claims:
- 在NTU120-AS online unconstrained测试设置下，ReGenNet的FID为11.00，远低于最佳基线MDM-GRU的24.25，准确率（0.749）与多模态指标（22.90）均达到最优。
- 在Chi3D-AS online unconstrained测试中，ReGenNet取得FID 13.76，显著优于MDM的18.40，且多样性（6.35）最接近真实数据。
- 在InterHuman-AS online unconstrained测试中，ReGenNet以FID 2.265超越此前最优的RAIG（FID 2.915）和MDM（FID 3.397），同时MM Dist（6.860）和Diversity（5.214）均最优。
- 消融实验表明，移除显式交互损失（w.o. L_inter）导致训练条件下的FID从0.90上升至1.96，测试条件下的准确率从0.749降至0.751，证明交互损失对生成质量的关键作用。
---

# ReGenNet: Towards Human Action-Reaction Synthesis

> [!tip] 核心洞察
> 将人类交互分解为行动者与反应者的非对称关系，利用扩散模型预测干净姿势，并直接对相对姿态、方向和根位移施加L2交互损失，从而大幅提升反应生成的即时性和物理一致性。

| 字段 | 内容 |
|------|------|
| 中文题名 | ReGenNet：面向人体动作-反应合成 |
| 英文题名 | ReGenNet: Towards Human Action-Reaction Synthesis |
| 会议/期刊 | CVPR 2024 |
| Links | [Project](https://liangxuy.github.io/ReGenNet/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | ReGenNet |
| Dataset | NTU120-AS, Chi3D-AS, InterHuman-AS |

> [!tip] 效果简介
> - NTU120-AS (online, unconstrained, test conditioned) 上，FID↓ 11.00 vs 24.25 (MDM-GRU) (-13.25)。
> - Chi3D-AS (online, unconstrained, test conditioned) 上，FID↓ 13.76 vs 18.40 (MDM) (-4.64)。
> - InterHuman-AS (online, unconstrained) 上，FID↓ 2.265 vs 2.915 (RAIG) (-0.65)。

## 概述

### 问题瓶颈

现有的人体运动生成方法在研究人类交互时普遍存在一个根本性盲区：它们将交互双方视为对称的、可互换的参与者，忽略了真实人际互动中**行动者（Actor）与反应者（Reactor）之间的非对称关系**。这种简化导致生成的反应动作缺乏即时性、物理一致性和身体细节的精细度。具体而言，三个关键瓶颈制约了该领域的发展：

1. **缺乏非对称建模**：现有数据集和模型不区分“谁先动、谁回应”，将交互简化为同步生成或随机分配角色，无法捕捉反应动作对行动者动作的条件依赖性。
2. **离线生成范式的局限**：主流方法（如基于Transformer编码器的扩散模型）依赖双向注意力，只能离线生成完整序列，无法满足AR/VR、游戏等场景对**在线、逐帧即时反应**的需求。
3. **交互语义的弱约束**：现有损失函数仅对独立关节位置施加监督，缺乏对交互双方相对姿态、朝向和空间位移的显式几何约束，导致生成的反应在接触距离、身体朝向等方面与行动者动作脱节。

### 核心方法

ReGenNet针对上述瓶颈提出了三个层级的解决方案，形成了“数据标注—架构设计—损失约束”的完整闭环：

- **非对称数据标注**：对NTU120、InterHuman和Chi3D三个数据集进行人工标注，明确指定每段原子交互中的行动者与反应者顺序，为模型学习非对称交互模式提供监督信号。
- **面向在线生成的Transformer解码器架构**：采用堆叠的Transformer解码器替代传统编码器，通过**方向性注意力掩码**（directional attention mask）防止未来信息泄漏，使模型能够以自回归方式逐帧生成反应，天然支持在线推理。
- **显式交互损失**：设计直接作用于相对关节位置、全局旋转矩阵差和根位移的L2损失函数，在扩散模型的预测干净样本上施加几何一致性约束，确保生成的反应在空间关系上与行动者动作保持物理合理。

模型采用SMPL-X身体表征，包含精细的手部姿态、面部表情和眼球旋转参数，使生成的反应具备丰富的身体细节。条件注入方式为：将行动者动作嵌入与加噪反应嵌入沿特征维拼接后通过线性层融合，同时扩散时间步和可选的动作标签经嵌入后求和，作为解码器的条件输入。

### 主要结果

在三个公开数据集上进行的在线、非约束（online, unconstrained）测试设置下，ReGenNet在所有核心指标上均显著超越现有最优方法：

| 数据集 | 指标 | ReGenNet | 最佳基线 | 提升幅度 |
|--------|------|----------|----------|----------|
| NTU120-AS | FID↓ | **11.00** | 24.25 (MDM-GRU) | −54.6% |
| Chi3D-AS | FID↓ | **13.76** | 18.40 (MDM) | −25.2% |
| InterHuman-AS | FID↓ | **2.265** | 2.915 (RAIG) | −22.3% |

在跨相机泛化测试中，ReGenNet的准确率从最佳基线的0.636提升至**0.713**，证明其鲁棒性并非源于对特定视角的过拟合。消融实验进一步揭示了关键设计的作用：移除显式交互损失使训练FID从0.90恶化至1.96；随机打乱行动者-反应者标注则显著降低所有指标，证实了非对称建模的必要性。此外，仅需**5个DDIM采样步骤**即可在0.76 ms内生成一帧，实现了质量与延迟的最优平衡。

### 方法谱系与知识库定位

ReGenNet处于**条件人体运动生成**与**人-人交互建模**的交叉地带，其方法谱系可沿以下维度定位：

| 维度 | 传统方法 | ReGenNet的差异化 |
|------|----------|------------------|
| 生成范式 | 离线双向生成（cVAE, Kingma et al., 2013; MDM, Tevet et al., 2022） | 在线自回归生成，通过解码器掩码保证因果性 |
| 交互建模 | 对称同步生成（InterGen, Liang et al., 2023）或文本驱动（RAIG, Tanaka et al., ICCV 2023） | 显式非对称行动者-反应者分解 |
| 身体表征 | SMPL或骨架关节（T2M, Guo et al., CVPR 2022） | SMPL-X，包含手部、面部和眼球细节 |
| 空间约束 | 无显式交互损失 | 相对姿态、朝向、位移的三项L2交互损失 |

该方法在知识库中的核心贡献在于：**首次将人类交互形式化为非对称的条件生成问题**，并通过扩散模型框架内的架构创新（解码器掩码）与损失函数设计（显式交互损失）实现了在线、物理一致的反应合成。其局限性主要体现在当前仅处理原子动作周期内的单向反应，尚未覆盖长时交互中的角色切换与意图转移，这为后续研究指明了方向。

## 背景与动机

### 问题背景：人体交互生成中的非对称性缺失

在增强现实、虚拟现实和游戏等应用中，虚拟角色不仅需要独立地执行动作，更需要对他人的行为做出即时、合理的反应。然而，现有的人体运动生成研究长期聚焦于单人动作合成或多人的对称性交互生成，忽略了真实人类交互中的一个核心特性：**非对称性**。在握手、击掌、躲避等原子交互中，总有一方先发起动作（行动者），另一方随后做出响应（反应者）。这种行动者-反应者的时序与语义差异，要求生成模型能够理解交互的因果关系，而非简单地将双方视为对等的运动序列。

### 现有方法的缺口

当前主流方法在人体动作-反应合成任务上存在三个关键瓶颈：

**1. 缺乏专用的非对称标注与基准。** 现有的人-人交互数据集（如NTU120、Chi3D、InterHuman）虽然包含丰富的交互动作，但均未显式标注行动者与反应者的身份。这导致模型在训练时无法学习交互的因果方向，只能将双方运动视为对称序列处理。实验证据表明，使用随机打乱的行动者-反应者标签训练会显著降低生成质量（Table 8），证实了非对称标注对任务至关重要。

**2. 模型架构不适应在线生成需求。** 基于Transformer编码器的方法（如MDM）采用双向注意力机制，在生成反应时需要访问完整的未来行动者信息，这使其只能用于离线场景。然而，真实应用要求反应者根据行动者已发生的动作即时响应，不允许“预知未来”。这一在线生成需求对模型架构提出了自回归约束，而现有方案缺乏相应的设计。

**3. 缺乏显式的空间交互约束。** 大多数方法仅依赖扩散模型的隐式学习来捕捉交互模式，未对反应者与行动者之间的相对姿态、朝向和空间位置施加直接监督。这导致生成的反应在细节上容易出现穿透、错位等物理不一致现象。

### 本文动机与核心思路

针对上述缺口，ReGenNet提出了一套系统性的解决方案。其核心洞察在于：**将人类交互显式分解为行动者与反应者的非对称关系，并围绕这一关系设计数据标注、模型架构和损失函数**。

具体而言，ReGenNet首先对NTU120、Chi3D和InterHuman三个数据集进行人工标注，明确每个原子交互中的行动者与反应者顺序。在模型层面，采用堆叠Transformer解码器替代编码器，通过方向性注意掩码防止未来信息泄漏，实现真正的在线反应生成。此外，引入显式的L2交互损失，直接监督相对关节位置、全局旋转和根位移，确保生成反应在几何与物理层面与行动者保持一致。这一“非对称标注 + 自回归架构 + 显式空间约束”的组合，使ReGenNet在多个基准上显著超越了现有方法。

## 核心创新

ReGenNet 的核心创新在于首次将人体动作-反应合成建模为**非对称、在线、细节丰富**的条件生成任务，并通过三个相互耦合的 changed slots 实现突破。

### 1. 非对称交互建模：从对称角色到显式行动者-反应者标注

现有交互生成方法（如 InterGen、RAIG）通常将交互双方视为对称角色，或随机分配行动者与反应者，忽略了真实交互中“一方发起、另一方即时响应”的非对称因果结构。ReGenNet 的关键洞察是：**行动者的运动序列是反应者运动的因果条件，而非对等输入**。

为此，作者对 NTU120、InterHuman 和 Chi3D 三个数据集进行了人工标注，显式标记每个原子交互中的行动者与反应者顺序（Table 1）。消融实验（Table 8）直接验证了这一设计的必要性：使用随机打乱的角色标签训练，性能显著劣于使用人工标注的版本，证实非对称标注对任务至关重要。

### 2. 在线生成架构：从双向编码器到方向注意掩码的 Transformer 解码器

传统条件运动扩散模型（如 MDM）采用 Transformer 编码器，其双向自注意力机制允许每一帧“看到”未来信息，因此只能用于离线生成——即已知完整行动者序列后一次性生成完整反应序列。然而，实际应用中反应者需要在行动者动作发生的瞬间即时响应，不允许访问未来帧。

ReGenNet 将核心网络替换为**堆叠 Transformer 解码器**，并引入**方向注意掩码**（directional attention mask），使每个时间步只能关注当前及过去的帧，从根本上防止未来信息泄漏。这一架构选择使模型天然支持自回归在线生成：给定已观测的行动者帧，逐帧生成即时反应。同时，条件注入方式从传统的交叉注意力改为将行动者嵌入与加噪反应嵌入沿特征维拼接后通过线性层融合，消融实验（Table 6, Add vs Concat）证实拼接策略优于加法融合。

### 3. 显式交互损失：从隐式学习到几何约束的直接监督

现有方法通常仅依赖扩散模型的像素级重建损失，缺乏对交互双方空间关系的显式建模。ReGenNet 提出**显式 L2 交互损失** $\mathcal{L}_{inter}$，直接监督以下三个几何量：

- **相对关节位置**：$\theta^{xy} = FK(\theta^y) - FK(\theta^x)$
- **相对全局旋转**：$q^{xy} = RM(q^y)^\top \cdot RM(q^x)$
- **相对根位移**：$\gamma^{xy} = \gamma^y - \gamma^x$

交互损失对预测反应与真实反应在上述三个量上的 L2 误差进行惩罚，确保生成的反应在空间位置、朝向和距离上与行动者保持物理一致性。消融实验（Table 6, w.o. $\mathcal{L}_{inter}$）表明，移除交互损失使训练条件下的 FID 从 0.90 恶化至 1.96，验证了显式几何约束对生成质量的关键作用。

### 4. 身体表示的精细化：从骨架到 SMPL-X

为生成细节丰富的反应，ReGenNet 采用 **SMPL-X 身体模型**作为数据表示，相比现有方法常用的 SMPL 或骨架关节，SMPL-X 额外包含精细的手部姿态、面部表情和眼球旋转参数。这使得模型能够生成包含手指动作和面部细节的反应，更贴近真实人-人交互场景。

### 创新耦合逻辑

上述四个 changed slots 并非孤立改进，而是形成因果闭环：非对称标注定义了“谁驱动谁”的条件方向 → Transformer 解码器+方向掩码保证了在线生成的时序因果性 → 显式交互损失确保生成的反应在几何空间上与行动者保持物理一致性 → SMPL-X 表示提供了足够的身体细节容量。这一耦合使 ReGenNet 在 NTU120-AS、Chi3D-AS 和 InterHuman-AS 三个基准上均以显著优势超越现有方法。

## 整体框架

ReGenNet 的整体 pipeline 围绕**条件扩散模型**构建，核心目标是从给定的行动者（actor）运动序列中即时生成对应的反应者（reactor）运动。该框架将人类交互建模为**非对称的动作-反应关系**，并通过三个关键设计实现高质量的在线生成：防止未来信息泄漏的方向注意掩码、将行动者特征与噪声反应特征沿特征维拼接的条件注入方式，以及直接监督相对空间关系的显式交互损失。

### 输入输出流

模型的输入包括：
- **行动者运动序列** $\boldsymbol{y}^{1:N}$：一段长度为 $N$ 的 SMPL-X 人体运动，包含身体姿态参数 $\boldsymbol{\theta}$、全局旋转 $\boldsymbol{q}$ 和根位移 $\boldsymbol{\gamma}$
- **噪声化的反应序列** $\boldsymbol{x}_t^{1:N}$：在扩散前向过程中被逐步添加高斯噪声的反应运动
- **扩散时间步** $t$ 和可选的动作标签 $a$：经嵌入后求和，作为条件信号注入解码器

输出为预测的**干净反应序列** $\hat{\boldsymbol{x}}_0^{1:N}$，同样以 SMPL-X 参数表示，包含精细的手部姿态、面部和眼球旋转。

### 核心模块关系

**1. 扩散框架（Diffusion Model）**

ReGenNet 采用标准的去噪扩散概率模型（DDPM）框架。前向过程按马尔可夫链逐步向真实反应序列添加高斯噪声：

$$q(x_t^{1:N} | x_{t-1}^{1:N}) = \mathcal{N}(x_t^{1:N}; \sqrt{\alpha_t} x_{t-1}^{1:N}, (1-\alpha_t) I)$$

反向过程由一个可学习的去噪网络 $F$ 负责从噪声序列中恢复干净反应，训练目标为最小化预测与真实反应之间的 L2 误差：

$$\mathcal{L}_{dm} = \mathbb{E}_{x_0 \sim q(x_0), t \sim [1,T]} [\| x_0 - F(x_t, y^{1:N}, t, a) \|_2^2]$$

**2. Transformer 解码器 $F$（去噪核心网络）**

不同于以往方法使用的双向 Transformer 编码器（仅支持离线生成），ReGenNet 采用**堆叠的 Transformer 解码器单元**，并施加**方向注意掩码**（directional attention mask）。这一掩码确保每一帧只能关注当前及过去的帧，杜绝未来信息泄漏，从而天然支持自回归式的在线生成（Figure 2(b)）。

![[assets/figures/papers/paper_list_l1724_ReGenNet_Towards_Human_Action_Reaction_Synthesis/figures/003_Figure_2.jpg]]
*Figure 2: The architecture of our proposed ReGenNet which is formulated in a diffusion-based framework with Transformer Decoder Units. The gray panel of (a) illustrates the whole diffusion model with the “Forward Diffusion” process and a stack of*

**3. 条件融合模块**

行动者特征 $\boldsymbol{y}^{1:N}$ 与噪声反应特征 $\boldsymbol{x}_t^{1:N}$ 分别通过全连接层投影到统一维度 $d$ 的潜在空间，随后沿特征维度**拼接**，再经线性层融合后送入 Transformer 解码器。消融实验（Table 6）证实，拼接方式优于加法方式，因为它保留了行动者与反应者特征的独立可区分性。

**4. 时间步与动作标签嵌入**

扩散时间步 $t$ 和可选的动作标签 $a$ 分别经嵌入层投影后**相加**，作为额外条件注入解码器。动作标签分支可根据应用场景灵活启用或移除——当行动者的意图对反应者可知时启用，否则移除。

**5. 显式交互损失 $\mathcal{L}_{inter}$**

这是 ReGenNet 区别于其他方法的关键设计。模型不仅通过 $\mathcal{L}_{dm}$ 学习反应运动本身，还直接对行动者与反应者之间的**相对空间关系**施加 L2 惩罚。具体地，对每一帧计算以下三项的相对量：

$$\theta^{xy} = FK(\theta^y) - FK(\theta^x); \quad q^{xy} = RM(q^y)^\top \cdot RM(q^x); \quad \gamma^{xy} = \gamma^y - \gamma^x$$

其中 $\theta^{xy}$ 为相对关节位置（通过前向运动学 $FK$ 计算），$q^{xy}$ 为相对旋转矩阵差，$\gamma^{xy}$ 为相对根位移。交互损失对预测反应与真实反应在这些相对量上的差异进行约束：

$$\mathcal{L}_{inter} = \frac{1}{N} \big( \sum_{i=1}^N \|\theta^{x_0 \to y} - \theta^{\hat{x}_0 \to y}\|_2^2 + \sum_{i=1}^N \|q^{x_0 \to y} - q^{\hat{x}_0 \to y}\|_2^2 + \sum_{i=1}^N \|\gamma^{x_0 \to y} - \gamma^{\hat{x}_0 \to y}\|_2^2 \big)$$

最终训练损失为两者的加权和：

$$\mathcal{L}_{all} = \mathcal{L}_{dm} + \lambda_{inter} \cdot \mathcal{L}_{inter}$$

消融实验（Table 6）表明，移除 $\mathcal{L}_{inter}$ 会使训练条件下的 FID 从 0.90 恶化至 1.96，证实了显式交互约束对生成质量的关键作用。

### 在线推理流程

推理时，ReGenNet 从纯高斯噪声 $\boldsymbol{x}_T^{1:N}$ 出发，在给定行动者序列的条件下，通过 DDIM 采样逐步去噪。得益于方向注意掩码，模型可在仅 5 个采样步骤（约 0.76 ms/帧）下完成高质量生成（Table 7），实现低延迟的在线反应合成。

### 补充图表

![[assets/figures/papers/paper_list_l1724_ReGenNet_Towards_Human_Action_Reaction_Synthesis/figures/001_Figure_1.jpg]]
*Figure 1: Illustration of our proposed ReGenNet, i.e., given a human motion sequence and generate the plausible human reactions, which will have broad applications in AR/VR and games*

## 核心模块与公式推导

ReGenNet 的核心由一个**条件扩散模型**与一个**堆叠 Transformer 解码器**构成，辅以显式交互损失，实现从任意行动者动作到反应者动作的在线生成。

### 1. 扩散框架与前向过程

ReGenNet 将反应生成建模为条件去噪扩散过程。设反应序列为 $\boldsymbol{x}^{1:N} = \{x^i\}_{i=1}^N$，行动者动作序列为 $\boldsymbol{y}^{1:N}$。前向过程逐步向反应序列添加高斯噪声，形成马尔可夫链：

$$q(x_t^{1:N} | x_{t-1}^{1:N}) = \mathcal{N}(x_t^{1:N}; \sqrt{\alpha_t} x_{t-1}^{1:N}, (1 - \alpha_t) I)$$

其中 $x_0^{1:N}$ 为真实反应，$x_T^{1:N}$ 近似为标准高斯噪声，$\alpha_t$ 为噪声调度参数。

### 2. Transformer 解码器与条件注入

去噪网络 $F$ 采用堆叠的 **Transformer 解码器单元**，其关键设计在于**方向性注意力掩码**——每个时间步只能关注当前及过去的帧，阻止未来信息泄漏，从而支持自回归式在线生成。

条件注入通过**特征维拼接**实现：将含噪反应 $x_t^{1:N}$ 与行动者动作 $y^{1:N}$ 分别经全连接层投影至维度 $d$，沿特征维拼接后输入解码器。扩散时间步 $t$ 与可选的动作标签 $a$ 经嵌入后求和，作为解码器的额外条件输入。

### 3. 扩散模型训练损失

扩散模型的训练目标是最小化真实反应 $x_0$ 与网络预测的干净反应之间的 L2 误差：

$$\mathcal{L}_{dm} = \mathbb{E}_{x_0 \sim q(x_0), t \sim [1,T]} [\| x_0 - F(x_t, y^{1:N}, t, a) \|_2^2]$$

网络 $F$ 直接预测干净姿势 $x_0$，而非预测噪声，这一设计选择有助于稳定训练。

### 4. 显式交互损失

为强制生成的反应在空间上与行动者保持物理一致性，ReGenNet 引入显式交互损失，直接监督两者之间的相对几何关系。首先计算行动者（上标 $y$）与反应者（上标 $x$）之间的：

- **相对关节位置**：$\theta^{xy} = FK(\theta^y) - FK(\theta^x)$，其中 $FK$ 为前向运动学函数，将姿态参数映射为关节位置；
- **相对旋转矩阵差**：$q^{xy} = RM(q^y)^\top \cdot RM(q^x)$，$RM$ 将旋转表示转为旋转矩阵；
- **相对根位移**：$\gamma^{xy} = \gamma^y - \gamma^x$。

随后，对真实交互（$x_0 \to y$）与预测交互（$\hat{x}_0 \to y$）之间的上述三项施加 L2 惩罚：

$$\mathcal{L}_{inter} = \frac{1}{N} \big( \sum_{i=1}^N \|\theta^{x_0 \to y} - \theta^{\hat{x}_0 \to y}\|_2^2 + \sum_{i=1}^N \|q^{x_0 \to y} - q^{\hat{x}_0 \to y}\|_2^2 + \sum_{i=1}^N \|\gamma^{x_0 \to y} - \gamma^{\hat{x}_0 \to y}\|_2^2 \big)$$

### 5. 总体训练目标

最终训练损失为扩散损失与交互损失的加权和：

$$\mathcal{L}_{all} = \mathcal{L}_{dm} + \lambda_{inter} \cdot \mathcal{L}_{inter}$$

其中 $\lambda_{inter}$ 为交互损失权重。消融实验证实，移除 $\mathcal{L}_{inter}$（即 $\lambda_{inter}=0$）会导致训练 FID 从 0.90 恶化至 1.96，验证了显式空间约束对生成质量的关键作用。

## 实验与分析

### 实验设置与评估协议

ReGenNet在三个经过行动者-反应者标注的数据集上进行评估：NTU120-AS、Chi3D-AS和InterHuman-AS。评估采用在线非约束（online unconstrained）设定作为主测试协议，即模型以自回归方式逐帧生成反应，且不提供真实反应序列作为上下文。此外，还报告了离线非约束、在线约束以及跨摄像头泛化设定下的结果。评估指标包括：

- **FID↓**：生成反应与真实反应分布之间的Fréchet Inception Distance，越低越好。
- **Acc.↑**：基于预训练动作识别模型的分类准确率，衡量生成反应的语义正确性。
- **Multimod.→**：多模态指标，越接近真实数据越好。
- **Diversity→**：生成样本的多样性，越接近真实数据越好。

所有竞争方法使用相同的动作识别模型和评价协议，生成样本数量与随机种子设定一致。

### 主实验结果

#### NTU120-AS基准

在NTU120-AS的在线非约束测试条件下，ReGenNet在所有指标上均大幅超越现有方法。如Table 2所示，ReGenNet的FID达到11.00，而此前最优的MDM-GRU为24.25，降幅达54.6%。准确率方面，ReGenNet以0.749领先于MDM-GRU的0.736，且多模态距离（22.90）最接近真实数据（22.07）。在训练条件下的FID更是低至0.90，表明模型能够精确拟合训练分布。

#### Chi3D-AS基准

在Chi3D-AS数据集上（Table 3），ReGenNet在测试条件下取得FID 13.76，显著优于MDM的18.40和MDM-GRU的22.58。值得注意的是，ReGenNet的多样性指标（6.35）在所有方法中最接近真实数据（6.92），说明生成的反应既准确又保持了合理的运动变化。训练条件下的FID仅为0.27，进一步验证了模型对高质量交互数据的拟合能力。

![[assets/figures/papers/paper_list_l1724_ReGenNet_Towards_Human_Action_Reaction_Synthesis/figures/005_Table_3.jpg]]
*Table 3: Comparison to state-of-the-arts on the online, unconstrained setting for human action-reaction synthesis on Chi3D-AS. ± indicates 95% confidence interval, → means that closer to Real is better. Bold indicates best result and underline indicates second best*

#### InterHuman-AS基准

InterHuman-AS是迄今最大规模的多人交互数据集，ReGenNet在该基准上同样表现最优（Table 4）。其FID为2.265，超越此前最优的RAIG（FID 2.915，Tanaka et al., ICCV 2023）和MDM（FID 3.397）。同时，多模态距离（6.860）和多样性（5.214）均达到最佳，证明ReGenNet在包含精细手部姿态的复杂交互场景中仍能生成高质量反应。

![[assets/figures/papers/paper_list_l1724_ReGenNet_Towards_Human_Action_Reaction_Synthesis/figures/006_Table_4.jpg]]
*Table 4: Comparison to state-of-the-arts on the online, unconstrained setting for human action-reaction synthesis on the InterHuman-AS dataset*

#### 跨摄像头泛化

Table 5展示了在NTU120-AS不同摄像头视角下的泛化结果。ReGenNet的准确率达到0.713，远高于MDM-GRU的0.636，证明模型并非过度拟合单一视角，而是学到了视角无关的交互表征。

### 消融实验

#### 显式交互损失的必要性

移除显式交互损失（w.o. L_inter）导致训练条件下的FID从0.90恶化至1.96，测试条件下的准确率从0.749降至0.751（Table 6 Loss行）。这表明显式对相对姿态、方向和位移施加L2约束，对于维持生成反应的物理一致性和交互语义至关重要。

![[assets/figures/papers/paper_list_l1724_ReGenNet_Towards_Human_Action_Reaction_Synthesis/figures/008_Table_6.jpg]]
*Table 6: Ablation studies on the online, unconstrained setting on the NTU120-AS dataset*

#### 条件融合策略

Table 6的Modules行对比了加法融合（Add）与拼接融合（Concat）。拼接方式在测试FID（11.00 vs 11.51）和准确率（0.749 vs 0.747）上均优于加法，验证了将actor嵌入与noised reaction嵌入沿特征维拼接后通过线性层融合的设计选择。

#### Transformer解码器深度

增加Transformer解码器层数（ℓ_dec）持续提升性能：从2层到8层，测试FID从12.14降至11.00，准确率从0.742升至0.749。但进一步增加到16层时，FID仅小幅降至10.85，边际收益递减（Table 6 Num. of ℓ_dec行）。

#### DDIM采样步数

Table 7显示，使用5个DDIM采样步骤即可取得最佳FID-延迟权衡，仅需0.76 ms即可生成一帧。减少至2步会导致FID从11.00上升至11.75，而增加至10步以上性能趋于饱和。这证明ReGenNet具备实时在线部署的潜力。

#### 行动者-反应者标注的必要性

Table 8对比了使用人工标注顺序与随机打乱顺序训练的效果。随机化标注导致FID从11.00恶化至14.41，准确率从0.749降至0.735，证实了非对称标注对任务的核心价值——模型必须明确知晓谁是行动者、谁是反应者，才能生成语义正确的反应。

### 定性分析

Figure 3展示了ReGenNet在多种交互场景下的生成结果。模型能够根据行动者的动作即时生成物理一致的反应：例如，当行动者出拳时，反应者做出格挡或闪避；当行动者递出物品时，反应者伸手接取。得益于SMPL-X表示，生成的反应保留了精细的手部姿态和身体细节。

### 失败模式与局限性

尽管ReGenNet在原子动作周期内表现优异，但仍存在以下局限：

1. **长时交互与角色切换**：当前基准测试仅覆盖原子动作周期，模型未处理长时交互中行动者与反应者角色的动态转换。例如，在连续多轮推搡场景中，角色可能频繁互换，现有框架无法对此建模。
2. **数据质量问题**：NTU120数据集通过姿态估计算法获得，存在关节噪声和人体穿透现象；面部表情不自然。这限制了生成反应在视觉细节上的真实感上限。
3. **意图建模缺失**：模型目前未显式建模行动者的意图转移或多人互动伙伴的动态切换，在真实AR/VR应用中可能无法应对复杂的社交场景。

### 关键图表结论

- **Table 2/3/4**：ReGenNet在三个基准的在线非约束设定下均取得最优FID和准确率，验证了非对称建模与显式交互损失的联合优势。
- **Table 6**：消融实验证实了拼接融合、显式交互损失和深层解码器对性能的关键贡献。
- **Table 7**：5步DDIM采样即可实现实时生成（0.76 ms/帧），为在线部署提供了效率保证。
- **Table 8**：行动者-反应者标注是不可或缺的先验，随机化顺序会显著损害生成质量。

![[assets/figures/papers/paper_list_l1724_ReGenNet_Towards_Human_Action_Reaction_Synthesis/figures/004_Table_2.jpg]]
*Table 2: Comparison to state-of-the-arts on the online, unconstrained setting for human action-reaction synthesis on NTU120-AS. ± indicates 95% confidence interval, → means that closer to Real is better. Bold indicates best result and underline indicates second best*

![[assets/figures/papers/paper_list_l1724_ReGenNet_Towards_Human_Action_Reaction_Synthesis/figures/010_Table_8.jpg]]
*Table 8: Ablation studies on the necessity of the explicit actorreactor order annotations on the NTU120-AS dataset*

![[assets/figures/papers/paper_list_l1724_ReGenNet_Towards_Human_Action_Reaction_Synthesis/figures/009_Table_7.jpg]]
*Table 7: Ablation Studies of the number of DDIM [60] sampling timesteps on the online, unconstrained setting on NTU120-AS*

### 补充图表

![[assets/figures/papers/paper_list_l1724_ReGenNet_Towards_Human_Action_Reaction_Synthesis/figures/007_Table_5.jpg]]
*Table 5: Generalization results to different viewpoints on the online, unconstrained setting on the NTU120-AS dataset*

![[assets/figures/papers/paper_list_l1724_ReGenNet_Towards_Human_Action_Reaction_Synthesis/figures/013_Figure_3.jpg]]
*Figure 3: Visualization of human action-reaction synthesis results. Blue for actors and Orange for reactors*

![[assets/figures/papers/paper_list_l1724_ReGenNet_Towards_Human_Action_Reaction_Synthesis/figures/002_Table_1.jpg]]
*Table 1: Human-human interaction datasets. Skel. denotes skeleton and AS denotes asymmetry*

![[assets/figures/papers/paper_list_l1724_ReGenNet_Towards_Human_Action_Reaction_Synthesis/figures/011_Table_9.jpg]]
*Table 9: Results on the offline, unconstrained setting on NTU120-AS. Bold indicates best result and underline indicates second best*

## 方法谱系与知识库定位

### 1. 问题定位与基线谱系

ReGenNet 处理的是一个此前未被显式建模的任务：**在线人体动作-反应合成**（online human action-reaction synthesis）。现有的人体运动生成方法主要集中在两类范式上，但均未解决非对称交互中的即时反应生成问题。

第一类是**单人或多人运动生成基线**。经典的条件变分自编码器 **cVAE**（Kingma et al., 2013）可作为离线或在线反应生成的朴素基线，但其隐变量建模难以捕捉高动态的交互细节。运动扩散模型 **MDM**（Tevet et al., 2022）及其结合 GRU 的变体 **MDM-GRU** 在在线设置下表现显著优于 cVAE，但 MDM 的 Transformer 编码器采用双向注意力，本质上只能进行离线生成；MDM-GRU 虽通过循环结构实现在线推理，仍缺乏对交互空间关系的显式约束。稀疏输入运动扩散模型 **AGRoL**（Du et al., 2023）同样参与在线生成对比，但其设计初衷并非交互场景。

第二类是**多人交互生成基线**。**InterGen**（Liang et al., 2023）和 **RAIG**（Tanaka et al., ICCV 2023）分别代表扩散生成和文本驱动角色感知生成路线。在 InterHuman-AS 基准上，RAIG 的 FID 为 2.915，是此前最优结果，但其生成范式并非在线即时反应。**T2M**（Guo et al., CVPR 2022）作为文本到动作基线也被纳入对比。

ReGenNet 与上述方法的根本差异在于：它将交互显式分解为**行动者与反应者的非对称关系**，并通过方向注意掩码实现严格的自回归在线生成，同时引入**距离驱动的显式交互损失**直接监督相对姿态、方向和位移。

### 2. 方法设计的关键差异点

下表总结了 ReGenNet 相对于基线的核心设计变更：

| 设计维度 | 基线方法 | ReGenNet | 证据锚点 |
|---------|---------|---------|---------|
| **角色建模** | 不区分行动者-反应者或随机分配 | 人工标注原子交互中的行动者-反应者顺序 | Table 8; Sec. 3.1 |
| **模型架构** | Transformer 编码器（双向注意力，仅离线） | 堆叠 Transformer 解码器 + 方向注意掩码，实现在线自回归 | Fig. 2; Sec. 3.2 |
| **条件注入** | 交叉注意力或分离式条件注入 | 将 actor 嵌入与 noised reaction 沿特征维拼接后线性融合 | Sec. 3.2; Table 6 |
| **空间约束** | 无显式空间约束 | 显式 L2 交互损失，直接监督相对关节位置、全局旋转与根位移 | Eq. (3)-(4); Table 6 |
| **身体表示** | SMPL 或骨架关节 | SMPL-X，包含精细手部姿态、面部和眼球旋转 | Sec. 3.1 |

其中，**非对称标注**的消融实验（Table 8）表明，使用随机打乱的行动者-反应者标签训练会明显劣于人工标注版本，证实了角色区分对任务的必要性。**显式交互损失**的移除使训练条件下的 FID 从 0.90 恶化至 1.96，测试准确率下降，验证了该损失对生成质量的关键作用（Table 6）。

### 3. 适用边界与局限

ReGenNet 在以下条件下表现出显著优势：

- **原子交互周期**：NTU120-AS、Chi3D-AS 和 InterHuman-AS 三个基准的在线非约束测试中，ReGenNet 的 FID 分别达到 11.00、13.76 和 2.265，均显著优于最佳基线（Table 2-4）。
- **跨视角泛化**：在 NTU120-AS 的跨相机泛化测试中，ReGenNet 的准确率达 0.713，远超 MDM-GRU 的 0.636（Table 5），证明其并非过度拟合单一视角。
- **低延迟推理**：使用 5 个 DDIM 采样步骤即可取得最佳 FID-延迟权衡，单帧生成仅需 0.76 ms（Table 7）。

然而，该方法存在以下明确局限：

1. **长时交互未覆盖**：基准测试仅覆盖原子动作周期，未处理长时交互中行动者-反应者角色的动态切换。模型目前无法显式建模意图转移或多人互动伙伴的切换。
2. **数据质量约束**：NTU120 数据集通过姿态估计算法获得，存在噪声和人体穿透现象，面部表情不自然。这限制了 SMPL-X 精细表示潜力的充分发挥。
3. **意图建模简化**：当前模型将行动者意图作为可选条件（action label），但在实际应用中，反应者通常无法获知行动者的真实意图，这一假设需要进一步放宽。

### 4. 开放问题

基于上述局限，以下问题值得后续探索：

- **长时多人交互扩展**：如何将方法扩展至更长时程、包含角色切换的多人交互场景？这可能需要引入角色状态机或图结构建模。
- **多模态数据融合**：能否利用高质量多模态数据（如包含自然面部表情和文本描述）进一步提升反应的真实感？当前 SMPL-X 的面部参数在 NTU120 上未能充分发挥。
- **延迟-质量权衡**：在真实在线应用（如 AR/VR）中，如何进一步平衡推理延迟与生成质量？5 步 DDIM 已取得良好折衷，但更激进的加速策略（如蒸馏）是否可行尚待验证。
- **意图不可知场景**：当行动者意图对反应者不可知时，如何设计更鲁棒的生成策略？当前模型在移除意图分支后仍可工作，但性能损失程度需要系统评估。

## 原文 PDF

![[paperPDFs/CVPR_2024/ReGenNet_Towards_Human_Action_Reaction_Synthesis.pdf]]
---
title: "DyaDiT: A Multi-Modal Diffusion Transformer for Socially Favorable Dyadic Gesture Generation"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/DyaDiT_A_Multi_Modal_Diffusion_Transformer_for_Socially_Favorable_Dyadic_Gesture_Generation.pdf
project_link: "https://puckikk1202.github.io/dyadit_hp/"
code_link: null
aliases:
- DyaDiT
tags:
- CVPR_2026
- topic/generative_models_diffusion
- topic/benchmarks_datasets_evaluation
- topic/generative_models_diffusion/diffusion_image_video
core_operator: 通过正交化交叉注意力（ORCA）分离两位说话者的音频流，并显式注入关系、人格等社交因素，以及可选的运动风格和伙伴动作条件。
primary_logic: 在扩散Transformer框架中，通过音频正交化消除冗余信息，并利用社交条件嵌入和运动字典，能够生成更具多样性、真实感和社交一致性的双边手势。
claims:
- DyaDiT在FD和Diversity指标上均显著优于ConvoFusion等基线模型
- "用户研究显示73.9%的参与者更偏好DyaDiT生成的手势，统计显著性p < 10^{-8}"
- Seamless Interaction Dataset 上 FD (Static)↓ = 6.40
- Seamless Interaction Dataset 上 FD (Kinetic)↓ = 1.37
---

# DyaDiT: A Multi-Modal Diffusion Transformer for Socially Favorable Dyadic Gesture Generation

> [!tip] 核心洞察
> 在扩散Transformer框架中，通过音频正交化消除冗余信息，并利用社交条件嵌入和运动字典，能够生成更具多样性、真实感和社交一致性的双边手势。

| 字段 | 内容 |
|------|------|
| 中文题名 | DyaDiT：面向社交友好型双向手势生成的多模态扩散Transformer |
| 英文题名 | DyaDiT: A Multi-Modal Diffusion Transformer for Socially Favorable Dyadic Gesture Generation |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2602.23165) · [Project](https://puckikk1202.github.io/dyadit_hp/) |
| Topic | #topic/generative_models_diffusion #topic/benchmarks_datasets_evaluation #topic/generative_models_diffusion/diffusion_image_video |
| Method | DyaDiT |
| Dataset | Seamless Interaction Dataset, User Study |

> [!tip] 效果简介
> - Seamless Interaction Dataset 上，FD (Static)↓ 6.40 vs 9.22 (ConvoFusion) (-2.82)；FD (Kinetic)↓ 1.37 vs 1.74 (ConvoFusion) (-0.37)；Diversity (Static)↑ 27.46 vs 18.33 (ConvoFusion) (+9.13)。
> - User Study (A/B Test) 上，Overall Quality Preference 73.9% vs 26.1% (ConvoFusion) (+47.8pp)；Relationship Consistency Preference 69.8% vs 30.2% (ConvoFusion) (+39.6pp)。

## 概述

### 问题瓶颈

现有双向对话手势生成方法通常将双人音频视为单一混合信号，忽略社交语境与双人交互动态，导致生成的手势缺乏社交感知力与多样性。这一瓶颈的核心在于：未能显式分离两位说话者的音频流，也未注入关系、人格等社交因素作为生成条件。

### 核心思路

**DyaDiT** 提出在扩散Transformer框架中，通过**音频正交化交叉注意力（ORCA）** 消除两位说话者音频间的冗余信息，并显式注入关系类型与人格评分等社交条件，同时引入可学习的离散运动字典提供风格感知的运动基元，从而生成更具多样性、真实感与社交一致性的双向手势。

### 方法定位

DyaDiT 相比现有基线（如 **ConvoFusion** 与 **Audio2PhotoReal**）的核心改进体现在四个维度：

- **音频处理**：从混合信号处理升级为 ORCA 模块，分离并融合双方音频线索。
- **社交语境注入**：从无显式社交因素到通过 FiLM 调制与交叉注意力注入关系与人格嵌入。
- **运动风格控制**：从无风格控制到引入可学习离散运动字典，推理时可通过分类器自由引导增强或关闭。
- **伙伴运动输入**：从仅依赖自身音频到可选地将对方手势序列作为额外条件。

方法谱系上，DyaDiT 属于**条件扩散生成模型**，在 DiT 骨干中整合多模态上下文（音频、社交因素、运动风格、伙伴动作），并通过 VQ-VAE 将连续运动压缩为离散潜变量以降低计算成本并捕捉长期依赖。

### 主要结果

在 **Seamless Interaction Dataset** 上，DyaDiT 在真实感与多样性指标上均显著优于 ConvoFusion：FD Static 从 9.22 降至 **6.40**，FD Kinetic 从 1.74 降至 **1.37**；Diversity Static 从 18.33 提升至 **27.46**，Diversity Kinetic 从 1.10 提升至 **1.38**（见 Table 1）。

用户研究进一步验证了生成手势的社交友好性：73.9% 的参与者更偏好 DyaDiT 的整体手势质量，69.8% 认为其关系一致性更优，统计显著性达 $p < 10^{-8}$（见 Figure 7）。

消融实验确认了各组件的贡献：移除 ORCA 导致 FD 上升；将离散运动字典替换为连续版本使多样性下降；移除伙伴运动条件则削弱了动作的响应性；无条件版本虽维持一定真实感，但多样性明显降低（见 Table 1）。

### 局限与开放问题

当前方法仅生成上肢手势（43 个关节），全局方向与平移置零，限制了全身动作的自然度。关系类型的聚类效果不如人格特征清晰，表明社会线索的解耦仍存在挑战。开放问题包括：如何对音频进行“中性化”处理以更好解耦社会线索与语音内容，以及如何在 IPC 标签完善后设计更丰富的交际动态捕捉模块。

## 背景与动机

### 问题背景：双边对话手势生成的挑战

在面对面交流中，非语言行为——尤其是手势——承载着丰富的社会语义，直接影响对话的自然度与社交感知。随着数字人、虚拟现实和具身智能体的快速发展，如何让虚拟角色在双边对话中生成与语音内容、社交关系及个性特征相匹配的手势，已成为人机交互领域的核心挑战之一。

与单说话者手势生成不同，双边对话场景引入了独特的复杂性：两位参与者的语音信号在时间上交错、重叠，手势不仅需要与自身语音同步，还需对伙伴的言语和行为做出响应。这种“听-说-动”的耦合关系使得手势生成必须同时考虑**语音内容**、**社交语境**和**人际动态**三个维度。

### 现有方法的缺口：混合信号与社交盲区

当前双边手势生成方法存在两个关键瓶颈：

**1. 音频处理的“混合信号”问题。** 现有方法通常将双边对话的音频视为单一混合信号进行处理，未能显式分离两位说话者的语音流。当一方插话或双方同时说话时，这种混合表示会导致音频特征高度冗余，模型难以准确判断“谁在说话”以及“当前语音归属于哪一方”。其直接后果是生成的手势在对话者切换时出现动作模糊或归属错误，降低了手势的真实感与同步性。

**2. 社交语境的缺失。** 人类手势并非仅由语音内容驱动——朋友间的随意挥手与商务场合的克制手势截然不同，外向者与内向者的肢体语言也存在系统性差异。然而，现有模型（如 **ConvoFusion** 和 **Audio2PhotoReal**）未显式利用关系类型、个性特征等社交因素作为生成条件，导致生成的手势缺乏社交感知力，在不同社交场景下表现出“千人一面”的单调模式。

上述缺口共同导致了两个核心指标的分化：**生成真实感（Fréchet Distance, FD）不足**与**动作多样性（Diversity）受限**。前者反映手势与真实人类行为的分布差距，后者衡量模型能否为同一段对话生成不同的合理手势——两者在现有方法中难以兼得。

### 本文动机：从社交感知到可控生成

针对上述瓶颈，本文提出 **DyaDiT**——一个面向社交友好型双向手势生成的多模态扩散Transformer。其核心动机可归纳为三个层面：

- **解耦音频流以消除冗余**：通过正交化机制分离两位说话者的音频特征，使模型获得清晰的“谁在说话”信号，从根本上解决混合信号带来的模糊性。
- **注入社交语境以实现感知生成**：显式地将关系类型（如朋友、家人、同事）和个性评分（如外向性、宜人性）作为条件嵌入生成过程，使手势能够随社交场景自适应变化。
- **引入运动风格控制以提升多样性**：通过可学习的离散运动字典和可选的伙伴运动条件，赋予模型风格感知与响应式生成能力，在保持真实感的同时显著扩展手势的多样性空间。

DyaDiT 的设计目标并非简单追求指标上的边际提升，而是试图在**真实感-多样性-社交一致性**的三元权衡中建立新的平衡——这一目标将通过定量实验（Table 1）和用户主观研究（Figure 7）得到验证。

## 核心创新

DyaDiT 的核心突破在于将双边对话手势生成从“单一混合音频信号驱动”推进到“社交语境感知的多模态条件生成”。现有方法（如 ConvoFusion、Audio2PhotoReal）通常将双人对话音频视为一个不可分割的混合流，忽略了两位说话者各自的语言/副语言线索以及他们之间的社交关系动态。这导致生成的手势缺乏个性化和社交一致性——例如，对朋友和对陌生人的手势反应在视觉上难以区分。

DyaDiT 通过四个关键的 **changed slots** 系统性地解决了上述瓶颈：

### 1. 音频正交化交叉注意力（ORCA）

这是最关键的架构创新。传统方法将两位说话者的音频特征简单拼接或融合，导致信息冗余和歧义——当一方在另一方说话时插话或重叠时，模型难以判断当前手势应由谁的语音主导。

DyaDiT 引入 ORCA 模块，其核心操作是将自身音频特征 $a_{\mathrm{self}}$ 投影到对方音频特征 $a_{\mathrm{other}}$ 的子空间上，并从自身特征中减去该投影分量：

$$a_{\mathrm{self}}^{\perp} = a_{\mathrm{self}} - \mathrm{Proj}_{a_{\mathrm{other}}}(a_{\mathrm{self}})$$

其中投影操作 $\phi(\mathbf{x}) = W_2 \sigma(W_1 \mathbf{x} + b_1) + b_2$ 由一个轻量级 MLP 实现。经过正交化后，两个音频流中的共享信息（如环境噪声、相似韵律模式）被抑制，各自的独特信息得到增强。随后，通过可学习的门控参数 $\sigma(\mathbf{W}_g)$ 自适应融合两个方向的交叉注意力输出：

$$f_{\mathrm{audio}} = \sigma(\mathbf{W}_g) \cdot h_{\mathrm{self\rightarrow other}} + (1 - \sigma(\mathbf{W}_g)) \cdot h_{\mathrm{other\rightarrow self}}$$

消融实验证实了这一设计的有效性：移除 ORCA 后，FD Static 从 6.40 升至 7.32，FD Kinetic 从 1.37 升至 1.79（Table 1），表明音频解耦对运动真实感有直接贡献。

### 2. 社交语境条件注入

此前的方法完全忽略了对话者的社会关系（朋友、家人、同事等）和人格特质（外向性、宜人性等）对手势风格的塑造作用。DyaDiT 首次将这些社交因素作为显式条件引入生成过程：关系类型和人格评分被编码为嵌入向量，通过 FiLM 调制和交叉注意力两种机制注入 DiT 的每个 Transformer 块。这使得模型能够学习到“对亲密朋友的手势更放松、幅度更大”或“高外向性个体手势更丰富”等社交-运动映射。

用户研究提供了强有力的主观证据：在关系一致性维度上，69.8% 的参与者更偏好 DyaDiT 生成的手势，而 ConvoFusion 仅获得 30.2% 的偏好（Figure 7）。无条件版本（Uncond）的 Diversity Static 降至 21.65（vs. 27.46），进一步表明社交条件的移除会显著削弱生成多样性（Table 1）。

### 3. 离散运动字典与风格控制

DyaDiT 引入了一个可学习的离散运动字典，存储一组运动基元 $\{d_k\}_{k=0}^n$。在生成过程中，对方音频特征通过交叉注意力与加权运动基元交互：

$$a_{\mathrm{other}}^{\prime} = \mathrm{CA}(a_{\mathrm{other}}, \sum_{k=0}^{n} m_k d_k) + a_{\mathrm{other}}$$

这一设计提供了风格感知的运动先验：不同的运动基元组合可以对应不同的交互风格（如主导型、顺从型、镜像型）。推理时，运动字典可通过分类器自由引导（CFG）选择性激活或关闭，赋予用户对生成风格的细粒度控制。

将离散字典替换为连续版本后，Diversity Static 从 27.46 降至 21.47（Table 1），证明离散基元能更好地捕捉交互风格的离散性和多样性。

### 4. 伙伴运动条件

DyaDiT 可选地以对方的手势序列作为额外条件输入，使生成的手势能够响应伙伴的当前动作。移除这一自我运动条件分支（w/o self）后，FD Kinetic 升至 1.48，Diversity Kinetic 降至 1.25（Table 1），表明伙伴运动信息对生成具有响应性和互动性的动作至关重要。

### 创新总结

上述四个 changed slots 并非孤立改进，而是围绕一个统一目标协同工作：**将双边手势生成从“听音频、出动作”的单模态映射，升级为“理解谁在说、和谁说、怎么说”的社交语境推理任务**。ORCA 解决了“谁在说”的歧义，社交条件注入了“和谁说”的语境，运动字典和伙伴条件则丰富了“怎么说”的表达空间。这一设计范式使 DyaDiT 在 FD（真实感）和 Diversity（多样性）两个通常存在 trade-off 的指标上同时取得显著提升（Table 1），并在用户研究中以 73.9% 的整体质量偏好大幅领先基线（$p < 10^{-8}$，Figure 7）。

## 整体框架

DyaDiT 是一个基于扩散Transformer（Diffusion Transformer, DiT）的双向手势生成框架，其核心设计目标是将多模态社交语境显式地注入生成过程，以产生社交感知力强且多样化的对话手势。整体pipeline围绕四个关键模块组织：运动分词器（Motion Tokenizer）、音频正交化交叉注意力（ORCA）、运动字典（Motion Dictionary）以及作为主干网络的DiT去噪模块。

### 输入与条件流

框架接收多源异构输入，形成层次化的条件信号：

1. **音频流**：两位说话者的原始音频分别经预训练编码器提取特征后，送入 ORCA 模块进行解耦与融合，生成清晰的音频条件表示。
2. **社交语境**：关系类型（如朋友、家人等）与人格评分（如外向性、亲和性）通过嵌入层编码，随后以 FiLM 调制和交叉注意力两种方式注入 DiT 的每一层，使手势生成对社交场景敏感。
3. **运动风格（可选）**：一个可学习的离散运动字典提供风格感知的运动基元，用于调节对方音频特征，实现对手势风格的显式控制。推理时可通过分类器自由引导（classifier-free guidance）增强或关闭该控制。
4. **伙伴运动（可选）**：以对方的手势序列作为额外条件输入，使模型能够生成具有响应性和交互一致性的自身手势。

### 潜空间压缩与扩散过程

为降低扩散模型在高维连续运动空间中的计算开销并捕捉长期时序依赖，DyaDiT 首先训练一个 VQ-VAE 运动分词器，将连续的上肢关节运动序列压缩为离散潜变量表示。扩散过程在该潜空间中进行：前向过程按标准 DDPM 框架逐步向潜变量添加高斯噪声，得到带噪潜变量 $\mathbf{x}_t = \sqrt{\bar{\alpha}_t} \mathbf{x}_0 + \sqrt{1 - \bar{\alpha}_t} \mathbf{\epsilon}$；反向过程则由 DiT 主干网络以条件 $\mathbf{c}$ 为引导，预测并去除噪声，训练目标为标准 $\epsilon$-预测损失：

$$\mathcal{L}_{\mathrm{diff}} = \mathbb{E}_{\mathbf{x}_0, t, \epsilon} \left[ \left\| \epsilon - \epsilon_{\theta}(\mathbf{x}_t, t, \mathbf{c}) \right\|_2^2 \right]$$

### DiT 主干与多模态融合

每个 DiT 块由自注意力层和交叉注意力层组成。自注意力层负责建模潜姿态序列内部的时序依赖；交叉注意力层则将前述多模态上下文信息（音频、社交嵌入、伙伴运动等）整合进去噪过程。这种设计使得网络能够在去噪的每一步都充分感知社交语境和交互动态，而非仅在输入端做一次条件注入。

### 关键模块的协同关系

ORCA 模块通过从自身音频中减去其在对方音频子空间上的投影（$a_{\mathrm{self}}^{\perp} = a_{\mathrm{self}} - \mathrm{Proj}_{a_{\mathrm{other}}}(a_{\mathrm{self}})$），消除双人音频流中的冗余成分，再经可学习门控机制自适应融合两个方向的交叉注意力输出。运动字典则利用加权运动基元对对方音频特征进行交叉注意力调节（$\mathrm{CA}(a_{\mathrm{other}}, \sum_{k=0}^{n} m_k d_k) + a_{\mathrm{other}}$），为手势生成提供风格层面的引导。两者分别从“语义清晰度”和“风格多样性”两个维度增强生成质量，消融实验证实移除 ORCA 会导致 FD 指标恶化，而将离散运动字典替换为连续版本则显著降低多样性（Table 1），验证了各模块的独立贡献与协同效应。

### 补充图表

![[assets/figures/papers/paper_list_l987_https_arxiv_org_abs_2602_23165/figures/002_Figure_2.jpg]]
*Figure 2: Overview of DyaDiT. DyaDiT conditions on multiple input modalities, including audio, partner motion, relationship type, and personality scores. It employs an Audio Orthogonalization Cross Attention (ORCA) module to obtain cleaner audio representations and a motion dictionary to guide style aware gesture generation*

## 核心模块与公式推导

### 3.1 扩散Transformer主干网络

DyaDiT采用基于去噪扩散概率模型（DDPM）框架的扩散Transformer（DiT）作为核心去噪网络。其训练目标为标准噪声预测损失：

$$\mathcal{L}_{\mathrm{diff}} = \mathbb{E}_{\mathbf{x}_0, t, \epsilon} \left[ \left\| \epsilon - \epsilon_{\theta}(\mathbf{x}_t, t, \mathbf{c}) \right\|_2^2 \right]$$

其中，$\mathbf{x}_0$ 表示由运动分词器压缩得到的干净潜变量序列，$t$ 为扩散时间步，$\epsilon \sim \mathcal{N}(0, \mathbf{I})$ 为高斯噪声，$\epsilon_{\theta}$ 为去噪网络，$\mathbf{c}$ 为多模态条件信号。前向扩散过程通过下式生成带噪潜变量：

$$\mathbf{x}_t = \sqrt{\bar{\alpha}_t} \mathbf{x}_0 + \sqrt{1 - \bar{\alpha}_t} \mathbf{\epsilon}$$

每个DiT块包含一个自注意力层用于建模潜变量序列内部的时序依赖，以及一个交叉注意力层用于整合多模态上下文信息。社交因素（关系类型和人格评分）通过FiLM调制和交叉注意力两种机制注入DiT块，使生成过程显式感知社交语境。

### 3.2 音频正交化交叉注意力（ORCA）

现有方法通常将双人对话音频视为单一混合信号处理，导致两位说话者的音频特征高度冗余，难以区分各自对手势生成的贡献。ORCA模块通过正交投影操作消除音频流之间的信息冗余，其核心操作为：

$$a_{\mathrm{self}}^{\perp} = a_{\mathrm{self}} - \mathrm{Proj}_{a_{\mathrm{other}}}(a_{\mathrm{self}})$$

该公式从自身音频特征 $a_{\mathrm{self}}$ 中减去其在对方音频特征子空间上的投影，得到正交化后的纯净特征 $a_{\mathrm{self}}^{\perp}$。投影操作由轻量级MLP实现：

$$\phi(\mathbf{x}) = W_2 \sigma(W_1 \mathbf{x} + b_1) + b_2$$

其中 $\sigma$ 为非线性激活函数。正交化后，两个方向（self→other和other→self）的交叉注意力输出通过可学习门控机制自适应融合：

$$f_{\mathrm{audio}} = \sigma(\mathbf{W}_g) \cdot h_{\mathrm{self\rightarrow other}} + (1 - \sigma(\mathbf{W}_g)) \cdot h_{\mathrm{other\rightarrow self}}$$

该门控机制允许模型根据对话动态灵活调整双方音频信息的权重，从而生成更具响应性的手势。消融实验（Table 1）表明，移除ORCA模块会导致FD指标显著上升（FD Static从6.40升至7.32，FD Kinetic从1.37升至1.79），验证了ORCA对提升运动真实感的关键作用。

### 3.3 运动字典（Motion Dictionary）

为实现风格感知的手势生成，DyaDiT引入可学习的离散运动字典。该字典由 $n$ 个运动基元 $\{d_k\}_{k=0}^{n}$ 组成，每个基元编码特定的运动模式。运动字典与DyaDiT联合训练，无需正交化约束，因为手势生成不需要严格的相位对齐。在推理时，运动字典可选择性激活，通过分类器自由引导进一步增强或关闭风格控制。

对方音频特征通过运动字典的加权基元进行交叉注意力调节：

$$a_{\mathrm{other}}^{\prime} = \mathrm{CA}(a_{\mathrm{other}}, \sum_{k=0}^{n} m_k d_k) + a_{\mathrm{other}}$$

其中 $m_k$ 为第 $k$ 个基元的权重系数，CA表示交叉注意力操作，残差连接保留了原始音频信息。消融实验（Table 1）显示，将离散运动字典替换为连续版本会导致Diversity Static从27.46降至21.47，证明离散运动基元能更好地捕捉多样的交互风格。

### 3.4 运动分词器（VQ-VAE）

为降低扩散模型在连续运动空间上的计算成本并捕捉长期时序依赖，DyaDiT首先训练VQ-VAE将连续运动序列压缩为离散潜变量表示。该分词器将原始43关节的上肢运动数据映射到紧凑的离散编码空间，扩散过程在该潜空间中进行，而非直接操作高维连续运动数据。

### 补充图表

![[assets/figures/papers/paper_list_l987_https_arxiv_org_abs_2602_23165/figures/003_Figure_3.jpg]]
*Figure 3: ORCA reduces ambiguity between the two audio streams, allowing DyaDiT to generate realistic motion even when one person interrupts the other during the conversation. The example demonstrates the generated motions adjusts naturally as the conversation shifts*

## 实验与分析

### 定量对比：DyaDiT 在真实感与多样性上全面领先

Table 1 报告了 DyaDiT 与基线模型在 Seamless Interaction Dataset 上的 Frechet Distance（FD）与 Diversity 指标对比。FD 越低表示生成运动与真实分布越接近，Diversity 越高表示手势变化越丰富。DyaDiT 在四项指标上均取得最优结果：

![[assets/figures/papers/paper_list_l987_https_arxiv_org_abs_2602_23165/figures/004_Table_1.jpg]]
*Table 1: Quantitative comparison of DyaDiT and baselines in terms of Frechet Distance (FD) and Diversity. Lower FD indicates ´ higher realism, and higher diversity values indicate more varied motion generation*

- **FD (Static)**：DyaDiT 达到 **6.40**，较 ConvoFusion 的 9.22 降低 2.82，降幅达 30.6%，表明生成手势的静态姿态分布更贴近真实数据。
- **FD (Kinetic)**：DyaDiT 为 **1.37**，较 ConvoFusion 的 1.74 降低 0.37，说明运动动态轨迹的真实感显著提升。
- **Diversity (Static)**：DyaDiT 达到 **27.46**，较 ConvoFusion 的 18.33 提升 9.13，增幅近 50%，证明模型能够生成更丰富的姿态变化。
- **Diversity (Kinetic)**：DyaDiT 为 **1.38**，较 ConvoFusion 的 1.10 提升 0.28，表明运动序列的时序多样性也得到增强。

值得注意的是，ConvoFusion 虽然 Diversity 较低，但其 FD 也偏高，说明该模型在追求“安全”生成时牺牲了运动丰富度。DyaDiT 同时在这两个通常存在 trade-off 的维度上取得突破，核心归因于 ORCA 模块提供的清晰音频条件与运动字典引入的风格基元。

### 消融实验：四个关键设计的贡献拆解

Table 1 的消融部分逐项验证了各组件的因果作用：

1. **移除 ORCA（w/o ORCA）**：FD Static 升至 7.32，FD Kinetic 升至 1.79，两项退化幅度最大。这证实 ORCA 通过音频正交化消除双方语音冗余成分，是提升运动真实感的核心机制。当两位说话者语音重叠或交替时，未经正交化的音频特征会引入歧义，导致模型生成模糊、缺乏针对性的手势。

2. **将离散运动字典替换为连续版本（MD contin）**：Diversity Static 从 27.46 骤降至 21.47，降幅达 21.8%。离散运动基通过将连续运动空间量化为可学习的基元，迫使模型在有限的风格原型中进行组合，从而更好地捕捉对话中多样化的交互风格。连续版本丧失了这种结构化先验，导致生成趋同。

3. **移除自我运动条件分支（w/o self）**：FD Kinetic 升至 1.48，Diversity Kinetic 降至 1.25。伙伴运动输入为模型提供了对方的实时动作信息，使其能够生成更具响应性和协调性的手势。缺失该条件时，模型无法感知伙伴的当前动作状态，导致生成的动作在时序上缺乏交互一致性。

4. **无条件版本（Uncond）**：移除关系与人格条件后，Diversity Static 降至 21.65，说明社交因素嵌入是驱动手势多样性的重要信号源。当模型无法区分“朋友间随意交谈”与“上下级正式对话”时，生成的手势会趋向平均化，丧失场景特异性。

### 定性分析：手势的多样性与真实感

Figure 4 展示了 DyaDiT、ConvoFusion 和 Audio2PhotoReal 在相同音频输入下的生成对比。DyaDiT 生成的手势在以下维度表现突出：

![[assets/figures/papers/paper_list_l987_https_arxiv_org_abs_2602_23165/figures/005_Figure_4.jpg]]
*Figure 4: Qualitative Results. Comparison of visualization results between DyaDiT, ConvoFusion [31], and Audio2PhotoReal [3]. The gestures generated by DyaDiT exhibit higher diversity and greater realism compared to the other methods*

- **姿态丰富度**：DyaDiT 的手势幅度更大、关节变化更明显，而 ConvoFusion 倾向于生成幅度较小的保守动作，Audio2PhotoReal 则常出现不自然的僵硬姿态。
- **社交一致性**：在不同关系类型和人格条件下，DyaDiT 的手势风格发生可感知的变化（Figure 5），例如高外向性人格条件下手势更开放、幅度更大，而低外向性条件下更收敛。这验证了社交条件嵌入通过 FiLM 调制和交叉注意力机制成功影响了生成分布。
- **时序协调性**：ORCA 模块使 DyaDiT 能在对方插话时仍生成合理的手势（Figure 3），避免因音频重叠导致的动作混乱。

![[assets/figures/papers/paper_list_l987_https_arxiv_org_abs_2602_23165/figures/007_Figure_5.jpg]]
*Figure 5: Visualization results under different personality score conditionings. All samples are generated using classifier-free guidance with CFG = 2.5*

### 用户研究：主观偏好显著

Figure 7 报告了 A/B 测试结果，参与者在 DyaDiT 与 ConvoFusion 之间进行盲评：

![[assets/figures/papers/paper_list_l987_https_arxiv_org_abs_2602_23165/figures/006_Figure_7.jpg]]
*Figure 7: A/B subjective evaluation percentages comparing our method with ConvoFusion[31] and with ground truth. Participants preferred our generated motion due to its more natural and socially aware conversational behavior*

- **整体质量偏好**：**73.9%** 的参与者更偏好 DyaDiT 生成的手势，仅 26.1% 选择 ConvoFusion（p < 10⁻⁸）。
- **关系一致性**：69.8% 认为 DyaDiT 的手势更符合对话双方的关系类型。
- **人格一致性**：66.7% 认为 DyaDiT 的手势更贴合设定的人格特征。

这三项指标均远超随机水平（50%），且统计显著性极高，说明 DyaDiT 在社交感知维度上的优势不仅体现在自动指标上，也能被人类观察者稳定感知。

### 失败模式与局限

尽管整体表现优异，DyaDiT 仍存在以下可观测的不足：

1. **仅生成上肢手势**：模型输出 43 个上肢关节，全局方向和平移被置零。这是因为数据集中下肢运动估计不准确，作者主动放弃了全身动作生成。这导致生成的角色在空间位置和下肢表现上缺乏自然度，尤其在需要身体重心转移的交互场景中显得不完整。

2. **社会线索解耦不彻底**：Figure 8 的 t-SNE 聚类显示，关系类型（朋友、家人等）的聚类效果不如人格特征清晰。这意味着模型对关系类型的区分能力有限，可能源于音频信号中关系线索本身较弱，或当前的条件注入机制不足以完全解耦关系与语音内容。

![[assets/figures/papers/paper_list_l987_https_arxiv_org_abs_2602_23165/figures/009_Figure_8.jpg]]
*Figure 8: t-SNE clustering results of Relationships (left), Personality Scores (right)*

3. **IPC 标签未被利用**：数据集提供的 Interpersonal Communication Dynamics 标签因噪声大且定义模糊被弃用。这导致模型无法捕捉更细粒度的交际意图（如“赞同”、“质疑”、“安抚”），限制了手势的语义精确性。待 IPC 标注质量提升后，设计 IPC 感知的条件模块是一个明确的改进方向。

## 方法谱系与知识库定位

### 任务定位与基线关系

DyaDiT 聚焦于**社交友好型双向手势生成**（dyadic gesture generation），即从双人对话音频中为两位说话者同时生成自然、上下文一致的上肢手势。该任务处于音频驱动人体运动生成与社交信号感知的交叉点，核心挑战在于如何从混合音频流中分离两位说话者的语音线索，并将关系、人格等社交因素显式注入生成过程。

现有基线方法主要分为两类。**ConvoFusion** 是目前代表性的双边手势生成模型，但其将双人对话音频视为单一混合信号处理，未显式建模社交语境或分离音频流，导致生成的手势缺乏社交感知力和多样性。**Audio2PhotoReal** 则将单说话者框架延伸至双人场景，同样未解决音频流混淆和社交条件注入问题。DyaDiT 与这些方法的**核心差异**在于：通过正交化交叉注意力（ORCA）模块实现音频流解耦，并首次将关系类型、人格评分等社交因素作为显式条件引入扩散Transformer框架。

### 核心技术贡献与因果机制

DyaDiT 的方法设计围绕一个**因果瓶颈**展开：双边对话音频中两位说话者的语音高度重叠，直接作为条件输入会导致冗余和歧义，使模型难以学习到与特定说话者匹配的手势模式。其解决方案由四个相互配合的模块构成：

1. **音频正交化交叉注意力（ORCA）**：通过从自身音频中减去在对方音频子空间上的投影（$a_{\mathrm{self}}^{\perp} = a_{\mathrm{self}} - \mathrm{Proj}_{a_{\mathrm{other}}}(a_{\mathrm{self}})$），消除冗余成分，再通过可学习门控机制自适应融合两个方向的交叉注意力输出。消融实验显示，移除ORCA会使FD Static从6.40升至7.32、FD Kinetic从1.37升至1.79，证实该模块对运动真实感的关键作用。

2. **社交条件注入**：将关系类型和人格评分通过FiLM调制和交叉注意力注入DiT模块，使生成手势能反映不同社交关系下的行为模式。无条件版本（Uncond）的Diversity Static降至21.65（完整模型为27.46），说明社交条件显著增强了生成多样性。

3. **离散运动字典（MD）**：提供可学习的运动基元，实现风格感知的手势生成。将离散字典替换为连续版本后，Diversity Static从27.46降至21.47，表明离散运动基能更好地捕捉多样交互风格。

4. **伙伴运动条件**：可选地将对方手势序列作为额外输入。移除该分支（w/o self）使FD Kinetic升至1.48、Diversity Kinetic降至1.25，证明伙伴运动输入有助于生成响应性更强的动作。

### 适用边界与局限

DyaDiT 的适用边界受以下因素制约：

- **运动范围受限**：仅生成上肢手势（43个关节），因数据集中下肢运动估计不准确而被抛弃；全局方向和平移置零，限制了全身动作的自然度。这意味着模型目前无法处理站立、行走等涉及下肢和空间位移的交互场景。

- **社交线索解耦不充分**：关系类型（朋友、家人等）的t-SNE聚类效果不如人格特征清晰（见Figure 8），表明从音频中解耦不同维度的社会线索仍存在挑战。此外，模型未使用数据集提供的IPC（人际传播动态）标签，因其噪声大且不明晰，导致无法利用更细粒度的交际意图信息。

- **数据集依赖**：模型在Seamless Interaction Dataset上训练和评估，其泛化到其他双人交互场景（如不同文化背景下的对话习惯、不同录音条件）的能力尚未验证。

### 开放问题

论文明确提出了若干值得后续探索的方向：

1. **音频中性化处理**：如何对音频进行“中性化”处理，以更好地解耦社会线索和语音内容，减少条件信号之间的冲突，是提升社交条件可控性的关键。

2. **全身动作生成**：如何构建大规模、高质量的双人全身交互数据集，以支持从手势拓展到全身动作生成，是突破当前运动范围限制的前提。

3. **IPC感知建模**：在IPC标签得到完善后，如何设计IPC感知的条件模块，以捕捉更丰富的交际动态（如话轮转换、反馈信号等），有望进一步提升生成手势的社交一致性。

## 原文 PDF

![[paperPDFs/CVPR_2026/DyaDiT_A_Multi_Modal_Diffusion_Transformer_for_Socially_Favorable_Dyadic_Gesture_Generation.pdf]]

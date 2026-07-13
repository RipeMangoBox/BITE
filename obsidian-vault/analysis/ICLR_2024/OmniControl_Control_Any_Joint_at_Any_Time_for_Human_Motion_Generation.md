---
title: OmniControl Control Any Joint at Any Time for Human Motion Generation
type: paper
paper_level: A
venue: ICLR
year: 2024
pdf_ref: paperPDFs/ICLR_2024/OmniControl_Control_Any_Joint_at_Any_Time_for_Human_Motion_Generation.pdf
project_link: https://neu-vi.github.io/omnicontrol/
code_link: null
aliases:
- OCAJAATHMG
tags:
- ICLR_2024
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 将生成的动作转换为全局坐标，通过分析函数直接衡量与控制信号的距离，并利用该距离的梯度对扩散过程的预测均值进行多步迭代扰动（空间引导）；同时结合可训练的 realism guidance 残差网络，调整所有关节以保持运动真实性和连贯性。
primary_logic: 空间引导与真实感引导高度互补：空间引导通过轻量的全局坐标分析梯度实现精准的空间约束满足，无需依赖不准确的相对位置转换；真实感引导则通过零初始化线性层连接的 Transformer 副本输出特征残差，隐式修正全身所有关节，解决了空间引导无法影响非受控关节的问题，从而在控制精度与运动自然度之间取得有效平衡。
claims:
- OmniControl 在骨盆控制任务上的平均误差（Avg. err.）相比最先进的 GMD 方法降低了 79.2%（0.0338 vs 0.1439）。
- 移除空间引导（w/o spatial）导致平均误差从 0.0385 急剧上升至 0.4137，充分证明空间引导是保证控制精度的决定性模块。
- 移除真实感引导（w/o realism）导致 FID 从 0.310 恶化至 0.692，运动真实性严重下降，且出现脚部滑动和肢体不连贯。
- HumanML3D 上 FID ↓ = 0.218 (Ours on pelvis)
---

# OmniControl Control Any Joint at Any Time for Human Motion Generation

> [!tip] 核心洞察
> 空间引导与真实感引导高度互补：空间引导通过轻量的全局坐标分析梯度实现精准的空间约束满足，无需依赖不准确的相对位置转换；真实感引导则通过零初始化线性层连接的 Transformer 副本输出特征残差，隐式修正全身所有关节，解决了空间引导无法影响非受控关节的问题，从而在控制精度与运动自然度之间取得有效平衡。

| 字段 | 内容 |
|------|------|
| 中文题名 | OmniControl：人体动作生成中的任意关节任意时间控制 |
| 英文题名 | OmniControl Control Any Joint at Any Time for Human Motion Generation |
| 会议/期刊 | ICLR 2024 |
| Links | [Project](https://neu-vi.github.io/omnicontrol/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | OmniControl |
| Dataset | HumanML3D, KIT-ML |

> [!tip] 效果简介
> - HumanML3D 上，FID ↓ 0.218 (Ours on pelvis) vs 0.475 (PriorMDM) (↓54.1%)；Avg. err. ↓ 0.0338 (Ours on pelvis) vs 0.1439 (GMD) (↓79.2%)；Foot skating ratio ↓ 0.0547 (Ours on pelvis) vs 0.0897 (PriorMDM) (↓39.0%)。
> - KIT-ML 上，FID ↓ 0.702 (Ours on pelvis) vs 0.851 (PriorMDM) (↓17.5%)；Avg. err. ↓ 0.0759 (Ours on pelvis) vs 0.2305 (PriorMDM) (↓67.1%)。

## 概要

**问题瓶颈**：现有基于扩散的文本条件人体动作生成模型（如 **MDM** (Tevet et al., 2023)、**PriorMDM** (Shafir et al., 2024)、**GMD** (Karunratanakul et al., 2023)）普遍采用相对姿态表示——骨盆位置相对于前一帧、其他关节相对于骨盆。这种表示方式导致 inpainting 类方法难以处理稀疏的骨盆约束，且无法对骨盆以外的关节施加全局空间控制，限制了灵活可控动作生成的能力。

**核心方案**：OmniControl 提出了一种混合引导机制，将空间引导与真实感引导相结合。空间引导将生成的动作转换至全局坐标，通过轻量分析函数直接衡量与控制信号的距离，并利用该距离的梯度对扩散过程的预测均值进行多步迭代扰动，实现精准的空间约束满足。真实感引导则引入一个可训练的 Transformer 副本，通过零初始化线性层向各注意力层输出特征残差，隐式调整全身所有关节以保持运动真实性和连贯性。两者高度互补，在控制精度与运动自然度之间取得有效平衡。

**方法定位**：OmniControl 是首个支持在单一模型中实现“任意关节、任意时间”灵活空间控制的人体动作生成方法，其空间引导与真实感引导的双支路设计为可控扩散生成提供了新的范式。

**主要结果**：在 HumanML3D 数据集上，OmniControl 的骨盆控制平均误差相比最先进的 GMD 降低了 79.2%（0.0338 vs 0.1439），FID 相比 PriorMDM 降低了 54.1%（0.218 vs 0.475），脚部滑动比率降低了 39.0%。消融实验表明，移除空间引导会导致控制精度急剧恶化（Avg. err. 从 0.0385 升至 0.4137），而移除真实感引导则使 FID 从 0.310 恶化至 0.692，充分验证了两个模块的必要性。



### 问题背景：文本条件人体动作生成

从自然语言描述生成逼真的人体动作序列是计算机视觉与图形学中的核心挑战。近年来，基于扩散模型的方法在该任务上取得了显著进展，代表性工作包括 **MDM**（Tevet et al., 2023）及其变体 **PriorMDM**（Shafir et al., 2024）。这些模型采用“相对姿态表示”——每个关节的位置以骨盆为参考系进行编码，骨盆自身则相对于前一帧定义——在纯文本到动作（text-to-motion）任务上展现出良好的生成质量。

然而，纯文本控制缺乏对生成动作的空间约束能力。在许多实际应用中，用户需要指定特定关节在特定时刻的空间位置，例如“人物在第 30 帧时左脚踩在台阶上”或“手腕始终保持在桌面高度”。这种“任意关节、任意时刻”的灵活空间控制需求，对现有方法构成了根本性挑战。

### 现有方法的瓶颈：相对表示与 Inpainting 的局限性

现有方法在处理空间控制信号时，普遍采用“在输入端将全局控制信号转换为相对位置，再通过 inpainting 方式注入”的策略。以 **GMD**（Karunratanakul et al., 2023）为代表的两阶段引导扩散模型，虽然支持稀疏的骨盆控制，但存在两个根本性缺陷：

1. **相对表示导致的控制不精确**：由于 inpainting 依赖生成过程中的中间位置进行相对坐标转换，而中间位置本身并不准确，这种“不准确的转换”会累积误差，使控制精度显著下降。这一问题在骨盆约束稀疏时尤为严重。

2. **无法控制骨盆以外的关节**：现有方法的设计仅针对骨盆关节，无法将空间控制扩展到手腕、脚踝、头部等其他关节。这从根本上限制了方法的应用场景。

更广泛地说，现有框架存在一个深层矛盾：相对姿态表示虽然在纯文生动作任务上性能优异，却天然排斥全局空间约束的融入。直接改用全局坐标表示进行生成则会导致模型崩溃，无法产生合理的人体姿态（见 Table 6 与 Figure 8 的证据）。

### 本文动机：在全局坐标中直接衡量与控制误差

OmniControl 的核心动机源于一个关键洞察：**空间约束的精确满足应当在全局坐标空间中完成，而非依赖于不准确的相对位置转换**。具体而言：

- **空间引导（Spatial Guidance）**：将扩散模型预测的干净运动 $x_0$ 转换为全局坐标，通过一个轻量的分析函数 $G$ 直接衡量与控制信号之间的加权 L2 距离，并利用该距离的梯度对扩散过程的预测均值 $\mu_t$ 进行多步迭代扰动。这一设计绕开了相对表示的转换误差，实现了精准的空间约束满足。

- **真实感引导（Realism Guidance）**：空间引导仅作用于受控关节，无法保证非受控关节的运动连贯性。为此，OmniControl 引入一个可训练的 Transformer 副本（通过零初始化线性层连接到原运动扩散模型的各注意力层），输出特征残差以隐式调整全身所有关节，从而在控制精度与运动自然度之间取得有效平衡。

这一“混合引导”设计使得 OmniControl 成为首个能够以单一模型实现对任意关节、任意时刻进行灵活空间控制的方法，同时保持生成动作的逼真度与物理合理性。



## 核心方法与创新机理

OmniControl 的核心创新在于提出了**混合引导（Hybrid Guidance）**机制，将空间引导（Spatial Guidance）与真实感引导（Realism Guidance）深度耦合，从根本上解决了现有扩散式文本条件人体动作生成模型在空间可控性上的两大瓶颈。

### 瓶颈与设计动机

现有方法（如 **MDM** (Tevet et al., 2023)、**PriorMDM** (Shafir et al., 2024)、**GMD** (Karunratanakul et al., 2023)）均采用相对姿态表示——骨盆位置相对于前一帧、其他关节相对于骨盆。这种表示在纯文本生成中表现良好，但引入空间控制信号时陷入困境：inpainting 类方法需要将全局控制信号转换为相对位置才能输入模型，而这一转换依赖于不准确的中间生成位置，导致误差累积；更致命的是，这种设计天然无法处理骨盆以外的关节控制，因为其他关节的“全局位置”在相对表示中缺乏直接对应。

OmniControl 的破局思路是**保持相对表示作为内部生成特征，但在输出端引入全局坐标分析**，通过两个高度互补的引导模块分别解决控制精度与运动真实性的矛盾。

### 核心创新一：空间引导（Spatial Guidance）——从“输入端 inpainting”到“输出端梯度扰动”

这是 OmniControl 与所有 baseline 最根本的**范式转换**。

**Baseline 做法**：将全局控制信号转换为相对位置，在模型输入端进行 inpainting 替换，依赖模型的重建能力来满足约束。这种方式对骨盆控制尚且勉强可用（GMD 仅支持 xz 平面），对其他关节则完全失效。

**OmniControl 做法**：在扩散去噪的每一步，将模型预测的干净运动 $\mathbf{x}_0$ 通过函数 $R(\cdot)$ 转换为全局坐标 $\pmb{\mu}^g$，直接与控制信号 $\pmb{c}$ 比较，利用一个轻量的分析函数 $G$ 计算加权 L2 距离：

$$G(\pmb{\mu}, \pmb{c}) = \frac{\sum_n \sum_j \sigma_{nj} \| \pmb{c}_{nj} - \pmb{\mu}_{nj}^g \|_2}{\sum_n \sum_j \sigma_{nj}}, \quad \pmb{\mu}^g = R(\pmb{\mu})$$

然后利用该距离对扩散预测均值 $\pmb{\mu}_t$ 的梯度进行多步迭代扰动：

$$\pmb{\mu}_t = \pmb{\mu}_t - \tau \nabla_{\pmb{\mu}_t} G(\pmb{\mu}_t, \pmb{c})$$

这一设计的精妙之处在于三点：
1. **绕过相对表示限制**：梯度计算发生在全局坐标空间，不依赖不准确的相对位置转换，任何关节的全局约束都可以直接处理；
2. **计算对象是 $\pmb{\mu}_t$ 而非 $\mathbf{x}_t$**：消融实验证实，若将梯度计算对象改为当前噪声状态 $\mathbf{x}_t$，平均误差从 0.0385 飙升至 0.2380（Table 3），因为 $\pmb{\mu}_t$ 是去噪后的“干净”估计，其梯度更稳定；
3. **动态迭代次数**：早期扩散步使用较少迭代（$K_e=10$），后期精细去噪时增加迭代（$K_l=500$），在精度与推理时间之间取得平衡（Figure 6）。

### 核心创新二：真实感引导（Realism Guidance）——隐式全身运动修正

空间引导虽然精准，但有一个天然局限：它只对受控关节施加梯度扰动，非受控关节完全不受影响。这导致当骨盆被严格控制时，其他关节可能出现僵硬、不连贯甚至脚部滑动等问题。

**Baseline 做法**：无显式调整机制，仅依赖 inpainting 后的重建，非受控关节的运动质量完全取决于扩散模型的泛化能力。

**OmniControl 做法**：引入一个可训练的 Transformer 编码器副本，接收文本提示 $p$ 和编码后的空间控制信号，通过**零初始化线性层**向原始运动扩散模型的每个注意力层输出特征残差。这些残差隐式地扰动所有关节的特征表示，使全身运动在满足空间约束的同时保持连贯与真实。

这一设计的核心机制是：
- **零初始化**确保训练初期真实感引导不干扰预训练的运动扩散模型，逐步学习如何微调；
- **逐层残差注入**使得修正信号可以影响所有 Transformer 层的特征，实现全身所有关节的密集隐式调整；
- **空间编码器 $\mathcal{F}$** 由四层线性层组成，独立对每帧的空间控制信号编码，并对无控制帧进行掩码（$f_n = o_n \mathcal{F}(c_n)$），使模型感知有效控制信号的位置。

### 两模块的互补关系

消融实验（Table 3）清晰揭示了二者的分工与互补：

| 配置 | Avg. err. ↓ | FID ↓ | Foot Skating ↓ |
|------|-------------|-------|----------------|
| 完整模型 (on all) | 0.0385 | 0.310 | 0.0608 |
| 移除空间引导 (w/o spatial) | **0.4137** | 0.363 | 0.0654 |
| 移除真实感引导 (w/o realism) | 0.0402 | **0.692** | 0.0684 |

- **空间引导是控制精度的决定性模块**：移除后平均误差升高约 10 倍（0.0385 → 0.4137），模型几乎丧失空间约束能力；
- **真实感引导是运动质量的保障模块**：移除后 FID 从 0.310 恶化至 0.692，Figure 5 的视觉对比显示出现明显的脚部滑动和肢体不连贯；
- 二者联合使用时，控制精度与运动自然度同时达到最优，证明了混合引导设计的有效性。

### 与最相关工作的本质差异

| 维度 | GMD (Karunratanakul et al., 2023) | OmniControl |
|------|-----------------------------------|-------------|
| 可控制关节 | 仅骨盆（xz 平面） | 任意关节任意时间 |
| 控制信号融入方式 | 输入 inpainting（依赖相对转换） | 输出梯度扰动（全局坐标分析） |
| 全身连贯性保障 | 无显式机制 | 可训练真实感引导残差网络 |
| 骨盆 Avg. err. (HumanML3D) | 0.1439 | **0.0338**（↓79.2%） |

这种从“输入端局部 inpainting”到“输出端全局梯度扰动 + 可训练全身修正”的范式转换，使得 OmniControl 首次实现了单一模型对任意关节、任意时刻、任意稀疏度的空间控制，同时保持生成运动的真实感。



OmniControl 的整体 pipeline 围绕一个核心设计展开：**在扩散模型的去噪过程中，通过“空间引导 + 真实感引导”的混合策略，将任意关节、任意时刻的稀疏空间控制信号融入文本条件的人体动作生成**。图 2 给出了该框架的完整概览。

### 输入与输出

模型的输入由两部分组成：

- **文本提示** $p$：描述期望的动作语义（如“一个人向前走”）。
- **空间控制信号** $\mathbf{c} \in \mathbb{R}^{N \times J \times 3}$：指定若干关节在若干帧上的三维全局位置（$N$ 为序列帧数，$J$ 为关节数）。控制信号可以是任意稀疏的——不同关节可以在不同时刻被控制，未受控的帧和关节通过二进制掩码标记。

模型的输出是一个长度为 $N$、姿态维度为 $D$ 的人体动作序列 $\mathbf{x} \in \mathbb{R}^{N \times D}$，采用**相对姿态表示**（骨盆相对前一帧、其他关节相对骨盆），这与基线 MDM 保持一致。

### 核心模块与数据流

OmniControl 的 pipeline 由以下四个关键模块串联而成，数据流遵循“扩散去噪 → 空间引导扰动 → 真实感引导残差注入”的顺序：

1. **运动扩散模型 $M$（基于 MDM）**  
   这是整个框架的骨干网络。在每一个扩散步 $t$，模型接收文本提示 $p$ 和带噪动作序列 $\mathbf{x}_t$，直接预测干净运动 $\mathbf{x}_0(\theta) = M(\mathbf{x}_t, t, p)$。随后，利用扩散后验公式从 $\mathbf{x}_0$ 和 $\mathbf{x}_t$ 计算出当前步的预测均值 $\boldsymbol{\mu}_t(\theta)$：
   $$\boldsymbol{\mu}_t(\theta) = \frac{\sqrt{\bar{\alpha}_{t-1}}\beta_t}{1-\bar{\alpha}_t} \mathbf{x}_0(\theta) + \frac{\sqrt{\alpha_t}(1-\bar{\alpha}_{t-1})}{1-\bar{\alpha}_t} \mathbf{x}_t$$
   该均值是后续两个引导模块共同的作用对象。

2. **空间引导（Spatial Guidance）**  
   空间引导是一个**无训练、基于分析函数的梯度扰动模块**。其运作逻辑如下：
   - 将预测均值 $\boldsymbol{\mu}_t$ 通过转换函数 $R$ 从相对姿态映射为全局坐标 $\boldsymbol{\mu}^g$。
   - 计算分析函数 $G(\boldsymbol{\mu}, \mathbf{c})$，衡量生成动作的受控关节位置与控制信号之间的加权 L2 距离：
     $$G(\boldsymbol{\mu}, \mathbf{c}) = \frac{\sum_n \sum_j \sigma_{nj} \| \mathbf{c}_{nj} - \boldsymbol{\mu}_{nj}^g \|_2}{\sum_n \sum_j \sigma_{nj}}$$
     其中 $\sigma_{nj}$ 为指示该帧该关节是否受控的二进制权重。
   - 利用 $G$ 对 $\boldsymbol{\mu}_t$ 的梯度进行多步迭代扰动：
     $$\boldsymbol{\mu}_t \leftarrow \boldsymbol{\mu}_t - \tau \nabla_{\boldsymbol{\mu}_t} G(\boldsymbol{\mu}_t, \mathbf{c})$$
     迭代次数 $K$ 随扩散步动态调整——早期扩散步（$t > T_s$）使用较少迭代 $K_e$，后期扩散步（$t \leq T_s$）使用较多迭代 $K_l$，以平衡推理效率与控制精度。

   这一模块的关键优势在于：**在全局坐标空间中直接衡量与控制信号的误差，避免了将控制信号转换为相对位置时因中间生成结果不准确而引入的累积偏差**。消融实验证实，将梯度计算对象从 $\boldsymbol{\mu}_t$ 改为 $\mathbf{x}_t$ 会导致平均控制误差从 0.0385 升至 0.2380（Table 3），说明在预测均值上做引导是保证精度的关键设计。

3. **真实感引导（Realism Guidance）**  
   空间引导仅对受控关节施加约束，无法保证非受控关节的运动自然度。真实感引导正是为解决这一问题而引入的**可训练模块**。
   
   其结构为运动扩散模型中 Transformer 编码器的一个**可训练副本**，通过以下方式与原始模型交互：
   - 输入：文本提示 $p$ 和经空间编码器 $\mathcal{F}$ 处理后的控制信号特征 $f_n = o_n \mathcal{F}(c_n)$（$o_n$ 为掩码标记）。
   - 在原始 Transformer 的每一注意力层，真实感引导模块通过**零初始化线性层**输出特征残差，添加到对应层的特征上。
   
   零初始化确保了训练初期真实感引导不干扰原始生成过程，随着训练推进，该模块逐渐学会**隐式调整全身所有关节**，使非受控部位的运动与受控关节保持协调。消融实验表明，移除真实感引导会导致 FID 从 0.310 恶化至 0.692，并出现明显的脚部滑动和肢体不连贯（Table 3, Figure 5）。

4. **空间编码器 $\mathcal{F}$**  
   一个由四层线性层组成的轻量网络，独立对每一帧的空间控制信号进行编码。对于无控制信号的帧，通过二进制掩码将其特征置零，使真实感引导模块能够感知“哪些帧、哪些关节存在有效控制”。

### 混合引导的协同机制

空间引导与真实感引导在功能上高度互补，共同解决了“控制精度”与“运动真实感”之间的经典权衡：

- **空间引导**负责“硬约束”：通过轻量的全局坐标分析梯度，以可解析的方式将受控关节精确拉向目标位置，无需依赖不准确的相对位置转换。但它无法影响非受控关节。
- **真实感引导**负责“软协调”：通过可训练的 Transformer 副本输出特征残差，隐式调整全身所有关节，使非受控部位的运动与受控关节保持物理合理性和语义连贯性。但它不直接保证精确的空间约束满足。

两者作用于同一扩散均值 $\boldsymbol{\mu}_t$，在每一个去噪步中依次施加影响，最终使生成的动作既贴合控制信号，又保持自然的运动模式。这种“分析梯度 + 学习残差”的混合范式是 OmniControl 在稀疏、多关节控制场景下取得显著性能提升（骨盆控制平均误差相比 GMD 降低 79.2%，FID 相比 PriorMDM 降低 54.1%）的核心架构创新。

### 补充图表

![[assets/figures/papers/paper_list_l1899_OmniControl_Control_Any_Joint_at_Any_Time_for_Human_Motion_Generation/figures/002_Figure_2.jpg]]
*Figure 2: Overview of OmniControl. Our model generates human motions from the text prompt and spatial control signal. At the denoising diffusion step, the model takes the text prompt and a noised motion sequence*



OmniControl 的核心由三个关键模块构成：**运动扩散模型 M**、**空间引导（Spatial Guidance）** 和 **真实感引导（Realism Guidance）**。三者协同工作，在保持运动自然度的前提下实现对任意关节、任意时刻的精确空间控制。

### 运动扩散模型 M

OmniControl 基于 MDM（Tevet et al., 2023）的扩散框架，采用相对姿态表示。与预测噪声的常规扩散模型不同，该模型直接预测最终干净运动 $\mathbf{x}_0$：

$$\mathbf{x}_0(\theta) = M(\mathbf{x}_t, t, p)$$

其中 $\mathbf{x}_t \in \mathbb{R}^{N \times D}$ 为第 $t$ 步的噪声运动序列（$N$ 为帧数，$D$ 为姿态维度），$p$ 为文本提示。扩散反向过程的转移概率为：

$$P_{\boldsymbol{\theta}}(\mathbf{x}_{t-1}|\mathbf{x}_t, p) = \mathcal{N}(\mu_t(\boldsymbol{\theta}), (1-\alpha_t)I)$$

后验均值 $\pmb{\mu}_t(\theta)$ 由预测的 $\mathbf{x}_0$ 和当前 $\mathbf{x}_t$ 共同计算：

$$\pmb{\mu}_t(\theta) = \frac{\sqrt{\bar{\alpha}_{t-1}}\beta_t}{1-\bar{\alpha}_t} \pmb{x}_0(\theta) + \frac{\sqrt{\alpha_t}(1-\bar{\alpha}_{t-1})}{1-\bar{\alpha}_t} \pmb{x}_t$$

### 空间引导（Spatial Guidance）

空间引导是保证控制精度的决定性模块。其核心思想是：**将生成的动作转换为全局坐标，直接衡量与控制信号的距离，并利用该距离的梯度对扩散均值进行多步迭代扰动**。

分析函数 $G$ 衡量生成运动与控制信号之间的加权 L2 距离：

$$G(\pmb{\mu}, \pmb{c}) = \frac{\sum_n \sum_j \sigma_{nj} \| \pmb{c}_{nj} - \pmb{\mu}_{nj}^g \|_2}{\sum_n \sum_j \sigma_{nj}}, \quad \pmb{\mu}^g = R(\pmb{\mu})$$

其中 $\pmb{c} \in \mathbb{R}^{N \times J \times 3}$ 为空间控制信号（各关节在各帧的 xyz 位置），$\sigma_{nj}$ 为指示第 $n$ 帧第 $j$ 个关节是否受控的二进制掩码，$R(\cdot)$ 为相对姿态到全局坐标的转换函数。

在每个扩散步，利用 $G$ 的梯度对预测均值进行 $K$ 次迭代扰动：

$$\pmb{\mu}_t = \pmb{\mu}_t - \tau \nabla_{\pmb{\mu}_t} G(\pmb{\mu}_t, \pmb{c})$$

控制强度 $\tau$ 定义为：

$$\tau = \frac{20 \hat{\Sigma}_t}{V}, \quad \hat{\Sigma}_t = \min(\Sigma_t, 0.01)$$

其中 $\Sigma_t$ 为扩散噪声水平，$V$ 为需控制的帧数，使控制强度随受控帧密度自适应调节。

为平衡精度与推理时间，迭代次数 $K$ 采用动态策略：

$$K = \begin{cases} K_e & \text{if } T_s \leq t \leq T, \\ K_l & \text{if } t \leq T_s. \end{cases}$$

论文设定 $K_e=10$、$K_l=500$、$T_s=10$：在扩散早期（高噪声阶段）使用少量迭代，在后期（低噪声阶段）使用大量迭代以精细贴合约束。

**关键设计选择**：梯度计算对象为预测均值 $\pmb{\mu}_t$ 而非当前噪声状态 $\mathbf{x}_t$。消融实验表明，改为对 $\mathbf{x}_t$ 求梯度会导致平均误差从 0.0385 急剧上升至 0.2380（Table 3），因为 $\pmb{\mu}_t$ 是对最终干净运动的更直接估计。

### 真实感引导（Realism Guidance）

空间引导仅影响受控关节，无法保证非受控关节的运动连贯性。真实感引导通过**可训练的 Transformer 副本**输出特征残差，隐式调整全身所有关节。

该模块是运动扩散模型中 Transformer 编码器的可训练副本，接收文本提示 $p$ 和编码后的空间控制信号。空间控制信号由四层线性层组成的空间编码器 $\mathcal{F}$ 独立对每帧编码，并对无控制帧进行掩码：

$$f_n = o_n \mathcal{F}(c_n)$$

其中 $o_n$ 为二进制掩码，标记该帧是否存在有效控制信号。

真实感引导模块通过**零初始化线性层**连接到原始 Transformer 的每一注意力层，输出特征残差添加到对应层。零初始化确保训练初期该模块不干扰预训练的运动扩散模型，随后逐步学习如何调整全身运动以保持真实感和连贯性。

消融实验证实，移除真实感引导（w/o realism）导致 FID 从 0.310 恶化至 0.692，且出现明显的脚部滑动和肢体不连贯（Table 3, Figure 5），验证了该模块在维持运动自然度方面的关键作用。

### 两模块的互补机制

空间引导与真实感引导高度互补：
- **空间引导**通过轻量的分析函数梯度实现精准的空间约束满足，无需依赖不准确的相对位置转换，但仅影响受控关节；
- **真实感引导**通过可训练模块输出特征残差，隐式修正全身所有关节，解决了空间引导无法影响非受控关节的问题。

二者共同构成了混合引导（Hybrid Guidance）机制，在控制精度与运动自然度之间取得有效平衡。

### 补充图表

![[assets/figures/papers/paper_list_l1899_OmniControl_Control_Any_Joint_at_Any_Time_for_Human_Motion_Generation/figures/003_Figure_3.jpg]]
*Figure 3: Detailed illustration of our proposed spatial guidance. The spatial guidance can effectively enforce the controlled joints to adhere to the input control signals*

![[assets/figures/papers/paper_list_l1899_OmniControl_Control_Any_Joint_at_Any_Time_for_Human_Motion_Generation/figures/004_Figure_4.jpg]]
*Figure 4: Detailed illustration of our proposed realism guidance. The realism guidance outputs the residuals w.r.t. the features in each attention layer of the motion diffusion model. These residuals can directly perturb the whole-body motion densely and implicitly*



## 实验与关键发现

### 主实验结果

OmniControl 在 HumanML3D 和 KIT-ML 两个基准上均展现出显著优势。Table 1 报告了 HumanML3D 测试集上的核心指标：在骨盆控制任务上，OmniControl（Ours on pelvis）的 FID 达到 0.218，相比 **PriorMDM**（Shafir et al., 2024）的 0.475 降低了 54.1%；平均控制误差（Avg. err.）为 0.0338，相比 **GMD**（Karunratanakul et al., 2023）的 0.1439 降低了 79.2%。脚部滑动比率（Foot skating ratio）从 PriorMDM 的 0.0897 降至 0.0547，降幅达 39.0%，表明生成的运动在物理合理性上亦有明显提升。

![[assets/figures/papers/paper_list_l1899_OmniControl_Control_Any_Joint_at_Any_Time_for_Human_Motion_Generation/figures/005_Table_1.jpg]]
*Table 1: Quantitative results on the HumanML3D test set. Ours (on pelvis) means the model is only trained on pelvis control. Ours (on all) means the model is trained on all joints. Joint (Average) reports the average performance over all joints. Joint (Cross) reports the performance over the cross combination of joints. → means closer to real data is better*

当模型在全部关节上训练（Ours on all）时，平均关节性能保持稳定：FID 为 0.310，Avg. err. 为 0.0404，Foot skating ratio 为 0.0608。值得注意的是，OmniControl 仅用单一模型即可处理任意关节的稀疏空间控制，而 GMD 仅支持骨盆的 xz 平面控制，MDM 和 PriorMDM 则完全无法处理骨盆以外的关节约束。

Table 2 中 KIT-ML 数据集的结果进一步验证了方法的泛化能力：Ours on pelvis 的 FID 为 0.702（PriorMDM 为 0.851），Avg. err. 为 0.0759（PriorMDM 为 0.2305），控制误差降低 67.1%。KIT-ML 作为较小规模的数据集，OmniControl 仍能保持稳定的控制精度和运动质量，说明方法未对特定数据分布过拟合。

![[assets/figures/papers/paper_list_l1899_OmniControl_Control_Any_Joint_at_Any_Time_for_Human_Motion_Generation/figures/006_Table_2.jpg]]
*Table 2: Quantitative results on the KIT-ML test set. Ours (on pelvis) means the model is only trained on pelvis control. Ours (on all) means the model is trained on all joints. Joint (Average) reports the average performance over all joints. → means closer to real data is better*

**公平性说明**：所有对比方法均使用真实运动轨迹作为空间控制信号。GMD 被重新训练以接受三维骨盆位置（xyz），而非其原始设计的仅 xz 平面约束。评估涵盖 5 种控制信号稀疏水平（1, 2, 5, 49, 196 关键帧），最终性能为所有密度的平均值。

### 消融实验

Table 3 报告了 HumanML3D 测试集上的消融结果，明确了空间引导与真实感引导各自的贡献及其互补性。

![[assets/figures/papers/paper_list_l1899_OmniControl_Control_Any_Joint_at_Any_Time_for_Human_Motion_Generation/figures/007_Table_3.jpg]]
*Table 3: Ablation studies on the HumanML3D test set*

**移除空间引导（w/o spatial）** 导致 Avg. err. 从 0.0385 急剧上升至 0.4137，升高约 10 倍，FID 也从 0.310 恶化至 0.394。这一结果直接证实空间引导是保证控制精度的决定性模块——仅靠真实感引导无法有效将受控关节拉向目标位置。其核心机制在于：空间引导将生成动作转换为全局坐标后直接计算与控制信号的 L2 距离，并通过该距离对扩散预测均值 $\pmb{\mu}_t$ 的梯度进行多步迭代扰动（式 (2)-(3)），避免了对不准确的中间相对位置的依赖。

**移除真实感引导（w/o realism）** 导致 FID 从 0.310 飙升至 0.692，脚部滑动比率从 0.0608 升至 0.1042，运动真实性严重下降。Figure 5 的视觉对比直观展示了这一退化：无真实感引导时，非受控关节出现僵硬、肢体不连贯和明显的脚部滑动。这揭示了空间引导的固有局限——它仅通过全局坐标梯度影响受控关节，对非受控关节无直接作用。真实感引导通过可训练的 Transformer 副本向运动扩散模型的各注意力层注入特征残差，隐式调整全身所有关节，从而维持运动整体的连贯性与自然度。

**梯度计算对象的选择**同样关键。将空间梯度的计算对象由预测均值 $\pmb{\mu}_t$ 改为当前噪声状态 $\mathbf{x}_t$（Gradient w.r.t $\mathbf{x}_t$），Avg. err. 从 0.0385 升至 0.2380，控制精度大幅下降。这是因为 $\pmb{\mu}_t$ 是扩散模型对干净运动的最佳当前估计，在其上进行扰动能更准确地逼近目标约束。

### 控制信号密度分析

Figure 7 展示了空间控制信号密度对各项指标的影响。随着控制关键帧数量从 1 增加到 196，OmniControl 的 FID 和 Foot skating ratio 保持稳定甚至略有改善，而 MDM 和 PriorMDM 则显著恶化。这一对比凸显了混合引导架构对稀疏信号的鲁棒性：真实感引导通过空间编码器 $\mathcal{F}$ 对无控制帧进行掩码（$f_n = o_n \mathcal{F}(c_n)$），使模型能感知有效控制信号的位置，避免对缺失约束的过度拟合。

![[assets/figures/papers/paper_list_l1899_OmniControl_Control_Any_Joint_at_Any_Time_for_Human_Motion_Generation/figures/010_Figure_7.jpg]]
*Figure 7: Varying the density of spatial signal. The performance is reported on pelvis control on the HumanML3D dataset with the x-axis in logarithmic scale. All metrics are the lower the better*

### 推理效率与超参数权衡

Figure 6 展示了空间引导超参数 $T_s$、$K_e$、$K_l$ 对推理时间与 Avg. Error 的权衡关系。论文采用的默认设置（$K_e=10, K_l=500, T_s=10$）在精度与效率之间取得了合理平衡：早期扩散步（$t > T_s$）仅进行 10 次迭代，后期精细去噪阶段（$t \leq T_s$）进行 500 次迭代。这种动态迭代策略（式 (4)）避免了在整个去噪过程中均匀分配计算资源。

![[assets/figures/papers/paper_list_l1899_OmniControl_Control_Any_Joint_at_Any_Time_for_Human_Motion_Generation/figures/009_Figure_6.jpg]]
*Figure 6: Balancing inference time and Avg. Error by varying Ts*

然而，Table 5 的推理时间分解显示，OmniControl 的总体推理时间约为 121 秒，其中空间引导的大量迭代和模型前向传播是主要瓶颈。这一延迟使其难以满足实时交互需求，构成了方法的主要局限之一。

![[assets/figures/papers/paper_list_l1899_OmniControl_Control_Any_Joint_at_Any_Time_for_Human_Motion_Generation/figures/012_Table_5.jpg]]
*Table 5: Inference time. We report the time for baselines and each submodule of ours. The MDM in Sub-modules means the motion generation model we use in each diffusion step. The MDM in Methods Overall is Tevet et al. (2023)*

### 失败模式与局限

尽管 OmniControl 在控制精度和运动质量上大幅超越现有方法，仍存在若干值得关注的失败模式：

1. **脚部滑动残留**：即使在完整模型下，Foot skating ratio 仍约为 5-6%（Table 1, Ours on all 为 0.0608），说明真实感引导未能完全消除物理不合理现象。这暗示当前的真实感引导主要通过数据驱动的方式学习运动模式，缺乏对接触力、质心平衡等显式物理约束的建模。

2. **多关节冲突未定义**：论文仅测试了骨盆、双脚、头部和双腕等 6 类关节的独立控制，未系统讨论多个关节控制信号相互冲突时的行为（例如同时约束左手和右手向相反方向运动），也未提出冲突消解机制。

3. **全局表示的性能代价**：Table 6 显示，直接使用全局姿态表示进行纯文生动作时，FID 从相对表示的 0.544 升至 3.537，性能严重下降。Figure 8 进一步展示了全局表示下模型产生的失败案例——人体姿态出现不合理扭曲。这说明 OmniControl 仍依赖相对表示作为内部特征空间，仅在空间引导阶段进行全局坐标转换，两种表示之间的切换可能引入模式混淆。

![[assets/figures/papers/paper_list_l1899_OmniControl_Control_Any_Joint_at_Any_Time_for_Human_Motion_Generation/figures/013_Figure_8.jpg]]
*Figure 8: With global pose representation, the model cannot produce reasonable human poses on the HumanML3D dataset*

![[assets/figures/papers/paper_list_l1899_OmniControl_Control_Any_Joint_at_Any_Time_for_Human_Motion_Generation/figures/014_Table_6.jpg]]
*Table 6: Text-to-motion evaluation on the HumanML3D (Guo et al., 2022a) dataset. Comparison between relative presentation (Guo et al., 2022a) and global representation (Liang et al., 2024)*

### 补充图表

![[assets/figures/papers/paper_list_l1899_OmniControl_Control_Any_Joint_at_Any_Time_for_Human_Motion_Generation/figures/008_Figure_5.jpg]]
*Figure 5: Visual comparisons of the ablation designs, our full model, and the baseline GMD*



## 定位与知识库关联

### 1. 问题瓶颈与核心突破

现有基于扩散的文本条件人体动作生成方法（如 **MDM**（Tevet et al., 2023）、**PriorMDM**（Shafir et al., 2024）、**GMD**（Karunratanakul et al., 2023））普遍采用相对姿态表示——骨盆位置相对于前一帧定义，其他关节位置相对于骨盆定义。这种表示方式在纯文本生成任务中表现出色，但在引入空间控制信号时暴露出根本性缺陷：inpainting 类方法必须先将全局空间约束转换为相对位置，而这一转换依赖于生成过程中不准确的中间骨盆位置，导致约束注入存在系统性偏差。更关键的是，该表示方式天然地将骨盆与其他关节绑定，使得对骨盆以外关节（如手腕、脚踝）施加独立的全局空间控制几乎不可行。

**OmniControl** 的瓶颈突破在于识别出“输入侧约束注入”与“相对姿态表示”之间的结构性冲突，并将约束作用点从输入侧转移到输出侧：在扩散去噪的每一步，将模型预测的干净动作 $x_0$ 转换为全局坐标，直接计算与控制信号的 L2 距离，并利用该距离的梯度对扩散预测均值 $\mu_t$ 进行扰动。这一设计绕开了相对坐标转换的误差累积，使得任意关节的任意时刻全局空间控制成为可能。

### 2. 方法差异对照

| 方法 | 控制对象 | 控制方式 | 表示空间 | 核心局限 |
|------|----------|----------|----------|----------|
| **MDM** (Tevet et al., 2023) | 仅骨盆（通过 inpainting） | 输入侧相对位置替换 | 相对姿态 | 无法控制其他关节；稀疏约束下精度低 |
| **PriorMDM** (Shafir et al., 2024) | 仅骨盆（组合先验增强） | 输入侧相对位置替换 | 相对姿态 | 同 MDM，且对稀疏约束仍敏感 |
| **GMD** (Karunratanakul et al., 2023) | 仅骨盆 xz 平面 | 两阶段引导扩散 | 相对姿态 | 不支持 y 轴控制；无法控制其他关节 |
| **OmniControl** | 任意关节任意时刻 | 输出侧全局坐标梯度引导 + 可训练真实感引导 | 相对姿态（内部）+ 全局坐标（引导） | 推理时间长；脚部滑动未完全消除 |

**GMD** 是此前最接近 OmniControl 目标的工作，但其设计存在两个根本限制：（1）仅支持骨盆的 xz 平面控制，忽略了垂直方向（y 轴）——论文为公平比较，重新训练了 GMD 以支持三维骨盆位置，但即便如此，其 Avg. err. 仍高达 0.1439，而 OmniControl 仅 0.0338；（2）GMD 的两阶段引导架构无法泛化到骨盆以外的关节，因为其引导机制同样依赖于相对姿态转换。

### 3. 技术路线定位

OmniControl 处于**扩散模型引导（Diffusion Guidance）** 与**人体运动生成**的交叉地带，其技术路线可拆解为两个互补的引导机制：

- **空间引导（Spatial Guidance）** 属于**分析梯度引导（Analytic Gradient Guidance）** 范式：在扩散采样过程中，利用一个可微的分析函数 $G(\mu, c)$ 衡量生成运动与控制信号的全局坐标距离，通过梯度下降对预测均值进行多步迭代扰动。这与分类器引导（Classifier Guidance）共享“利用外部信号梯度修正采样过程”的思想，但区别在于：OmniControl 的分析函数 $G$ 无需训练，直接基于运动学转换 $R(\cdot)$ 和 L2 距离计算，且梯度作用于预测均值 $\mu_t$ 而非噪声状态 $x_t$——消融实验证实，将梯度计算对象改为 $x_t$ 会导致 Avg. err. 从 0.0385 升至 0.2380（Table 3），说明 $\mu_t$ 作为“当前最佳干净运动估计”是更合适的引导锚点。

- **真实感引导（Realism Guidance）** 属于**特征残差注入（Feature Residual Injection）** 范式：构建原 Transformer 编码器的可训练副本，接收文本提示和编码后的空间控制信号，通过**零初始化线性层**向原模型各注意力层输出特征残差。零初始化确保训练初期不破坏预训练生成能力，而残差形式允许模型隐式地调整全身所有关节——包括那些未被空间信号直接控制的关节——以维持运动真实性和肢体连贯性。这一设计可视为对 ControlNet 思想的轻量级适配，但针对序列生成任务做了关键简化：不引入额外的编码器分支，而是直接复用并微调原模型的 Transformer 结构。

### 4. 适用边界与局限

**适用边界：**
- 支持任意 SMPL/HumanML3D 关节（22/21 个关节）在任意时间帧上的三维空间控制，单模型覆盖所有关节类型。
- 控制信号密度可从 1 帧到全序列（196 帧）灵活变化，且实验表明密度增加时 FID 和 Foot skating ratio 保持稳定甚至改善（Figure 7）。
- 在两大数据集 HumanML3D 和 KIT-ML 上均验证有效，展现出一定的数据集泛化能力。

**已识别的局限：**
1. **推理效率瓶颈**：完整推理约需 121 秒（Table 5），主要开销来自空间引导的后期大迭代量（$K_l=500$）和多次模型前向传播。超参数分析（Figure 6）表明可通过调整 $T_s$、$K_e$、$K_l$ 在精度与速度间权衡，但距离实时交互仍有数量级差距。
2. **物理合理性残留问题**：尽管真实感引导将脚部滑动比率从 0.692（w/o realism 的 FID 对应）降至约 5-6%，但未完全消除。当前真实感引导仅学习“看起来真实”的运动模式，缺乏对物理约束（如接触力、质心平衡）的显式建模。
3. **控制冲突未定义**：论文仅测试了单关节控制场景，未系统讨论多个关节控制信号相互冲突时的行为（例如同时约束左手和右手向相反方向移动）。模型缺乏显式的优先级或冲突消解机制。
4. **全局表示的内部矛盾**：纯文本生成时，全局姿态表示的性能显著低于相对表示（Table 6），甚至无法生成合理的人体姿态（Figure 8）。OmniControl 因此仍以相对表示为内部特征空间，仅在引导阶段转换为全局坐标，这可能导致训练与推理时的特征分布不一致。
5. **关节覆盖不完整**：虽然声称支持“任意关节”，但实验仅覆盖骨盆、双脚、头部和双腕共 6 类关节，未对所有 22/21 个关节的组合控制进行系统性验证。

### 5. 开放问题与后续方向

1. **推理加速**：空间引导的迭代本质使其天然适合蒸馏或提前停止策略。是否可以将 $K_l$ 步迭代的知识蒸馏到更少的步骤中，或训练一个轻量预测网络直接输出扰动后的 $\mu_t$，从而将推理时间压缩至秒级？
2. **物理感知的真实感引导**：当前真实感引导仅以生成数据的统计真实感为目标。若能引入物理模拟器反馈（如脚部接触状态、质心投影），将物理合理性作为额外的训练信号，有望从根本上消除脚部滑动等伪影。
3. **多关节冲突消解**：当多个关节同时被控制且约束不一致时，空间引导的梯度可能相互对抗。需要研究是否可通过引入关节优先级权重、约束松弛机制或基于物理的协调损失来调和冲突。
4. **多人物交互扩展**：该方法的核心组件（全局坐标转换 + 分析梯度引导）在概念上可扩展到多人物场景，但需要解决人物间相对坐标定义、碰撞避免以及计算复杂度随人物数量线性增长的问题。
5. **控制信号自动生成**：在下游应用（如场景交互、VR 操控）中，手动指定空间控制信号成本高昂。如何从场景几何、交互意图或自然语言描述中自动推断合理的空间约束，是实现该方法大规模应用的关键前提。



## 原文 PDF

![[paperPDFs/ICLR_2024/OmniControl_Control_Any_Joint_at_Any_Time_for_Human_Motion_Generation.pdf]]

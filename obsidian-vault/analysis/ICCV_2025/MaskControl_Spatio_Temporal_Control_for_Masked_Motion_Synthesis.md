---
title: "MaskControl: Spatio-Temporal Control for Masked Motion Synthesis"
type: paper
paper_level: A
venue: ICCV
year: 2025
pdf_ref: paperPDFs/ICCV_2025/MaskControl_Spatio_Temporal_Control_for_Masked_Motion_Synthesis.pdf
project_link: null
code_link: null
aliases:
- MaskControl
tags:
- ICCV_2025
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 通过 Logits Regularizer（训练时隐式扰动 logits）和 Logits Optimization（推理时显式优化 logits），结合可微期望采样，可以调节掩码模型的 token 分布以精确跟随控制信号。
primary_logic: 控制令牌分类器的 logits 分布，而非直接在连续运动空间添加条件，可以在保持掩码模型强大文本至运动生成先验的同时，实现高精度、灵活且可零样本泛化的空间/时间控制。
claims:
- MaskControl 将 FID 从 TLControl 的 0.271 降至 0.061（降低 77%），同时平均误差从 1.08 cm 降至 0.91 cm。
- 消融实验表明，去除 Logits Regularizer 会导致 FID 升高至 0.142，证明其对保持质量至关重要。
- 在零样本目标控制任务中，MaskControl 在所有三个 HSI 任务上的约束误差均优于 ProgMoGen，并在 Head Height Constraint 上实现零误差。
- HumanML3D 上 FID (Pelvis Control) = 0.061
---

# MaskControl: Spatio-Temporal Control for Masked Motion Synthesis

> [!tip] 核心洞察
> 控制令牌分类器的 logits 分布，而非直接在连续运动空间添加条件，可以在保持掩码模型强大文本至运动生成先验的同时，实现高精度、灵活且可零样本泛化的空间/时间控制。

| 字段 | 内容 |
|------|------|
| 中文题名 | MaskControl：面向掩码动作合成的时空控制 |
| 英文题名 | MaskControl: Spatio-Temporal Control for Masked Motion Synthesis |
| 会议/期刊 | ICCV 2025 |
| Links | [paper](https://openaccess.thecvf.com/content/ICCV2025/html/Pinyoanuntapong_MaskControl_Spatio-Temporal_Control_for_Masked_Motion_Synthesis_ICCV_2025_paper.html) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | MaskControl |
| Dataset | HumanML3D, HSI-1, HSI-2, HSI-3 |

> [!tip] 效果简介
> - HumanML3D 上，FID (Pelvis Control) 0.061 vs 0.271 (TLControl) (减少 0.210 (-77%))；Average Error (cm) (Pelvis Control) 0.91 vs 1.08 (TLControl) (减少 0.17 cm)；R-Precision Top-3 (Pelvis Control) 0.809 vs 0.779 (TLControl) (增加 0.03)。
> - HumanML3D (Upper Body Editing) 上，FID 0.074 vs 0.103 (MMM), 1.213 (OmniControl) (优于所有对比方法)。
> - HSI-1 (Head Height Constraint) 上，Constraint Error 0.000 vs 0.012 (ProgMoGen) (降至零)。

## 概要

文本到运动生成领域长期面临一个核心瓶颈：**现有的可控运动生成方法难以同时实现高精度关节控制与高质量运动生成，且生成速度较慢**。主流方案大多基于扩散模型（如 **GMD**、**OmniControl**、**MotionLCM**），它们在连续运动空间或潜在空间中施加条件，虽然取得了一定进展，但往往以牺牲运动质量（高 FID）或控制精度为代价。前馈 Transformer 方法 **TLControl** 通过测试时优化实现了较高精度，但生成质量仍不理想（FID=0.271）。另一方面，基于掩码的运动模型（如 **MoMask**）在文本条件生成上展现了强大的先验能力和快速生成优势，却完全缺乏空间控制能力。

**MaskControl** 首次将可控性引入生成式掩码运动模型，通过一个关键洞察解决了上述矛盾：**控制 token 分类器的 logits 分布，而非直接在连续运动空间添加条件**。具体而言，方法引入两大核心机制——**Logits Regularizer**（训练时隐式扰动 logits，使运动 token 分布向控制信号对齐）和 **Logits Optimization**（推理时通过梯度下降显式优化 logits），配合 **可微期望采样（DES）** 实现离散 token 空间中的端到端梯度流动。这一设计使得模型能够在保持掩码模型强大文本-运动生成先验的同时，实现高精度、灵活且可零样本泛化的时空控制。

在 HumanML3D 基准上，MaskControl 取得了显著突破：**FID 从 TLControl 的 0.271 降至 0.061（降幅 77%），同时平均关节控制误差从 1.08 cm 降至 0.91 cm**。在全关节训练设置下，FID 为 0.083，显著优于 OmniControl（0.310）和 TLControl（0.256）。在零样本目标控制任务中，MaskControl 在三个 HSI 任务上的约束误差均优于可编程运动模型 **ProgMoGen**，并在 Head Height Constraint 上实现零误差。消融实验进一步证实，Logits Regularizer 对保持生成质量至关重要——去除该模块后 FID 升至 0.142。

方法支持三种应用场景：任意关节任意帧控制、身体部位时间轴控制、以及零样本任意目标函数控制，展现出从空间约束到语义级编程的广泛适用性。

### 可控运动生成的核心矛盾：精度与质量的权衡

文本驱动的 3D 人体运动生成近年来取得了显著进展，但在引入空间控制信号（如指定关节在特定时刻的位置）时，现有方法面临一个根本性瓶颈：**高精度控制与高质量生成难以兼得**。

当前可控运动生成的主流范式建立在扩散模型之上。**GMD**（Karunratanakul et al., ICCV 2023）仅支持根关节轨迹控制，控制粒度粗糙；**OmniControl**（Xie et al., 2023）通过 ControlNet 架构扩展到任意关节的任意时刻控制，但生成质量显著下降；**TLControl**（Wan et al., 2023）采用前馈 Transformer 加测试时优化，虽然实现了较高的控制精度（平均误差 1.08 cm），却以牺牲生成质量为代价（FID 高达 0.271）。这些方法的共同困境揭示了一个深层矛盾：在连续运动空间上施加条件约束，往往会破坏模型已学到的运动先验分布。

### 掩码运动模型的潜力与缺失

与此同时，基于掩码建模的运动生成方法展现出了强大的文本到运动生成能力。**MoMask**（Guo et al., 2023）等掩码运动模型通过离散 token 表示和迭代去掩码过程，在生成质量上显著优于扩散模型。然而，这类模型缺乏对空间控制信号的响应机制——它们只能根据文本描述生成运动，无法精确指定关节位置。

这一空白构成了本文的直接动机：**能否在不牺牲掩码模型生成质量的前提下，赋予其高精度的时空控制能力？**

### 控制机制的关键洞察

MaskControl 的核心洞察在于**控制信号的注入位置**。现有方法通常在连续运动空间上施加条件，这相当于直接修改生成结果。而掩码模型的操作空间是离散 token 的 logits 分布——一个定义在码本上的分类分布。如果能在 logits 层面调节 token 的采样概率，使其倾向于解码出符合控制信号的运动，就可以在保持文本条件运动先验的同时实现精确控制。

这一思路衍生出两个关键操作：训练时的 **Logits Regularizer**（隐式扰动 logits 以对齐控制信号）和推理时的 **Logits Optimization**（通过梯度下降显式优化 logits 以最小化控制误差）。两者的结合使得 MaskControl 成为首个在掩码运动模型上实现可控生成的方法，且支持零样本泛化到未见过的控制目标函数。

## 核心方法与创新机理

MaskControl 的核心创新在于将**可控性首次引入生成式掩码运动模型**，而非沿袭主流基于扩散的控制范式。其关键洞察是：通过操纵掩码 Transformer 输出端的 **logits 分布**，而非在连续运动空间直接施加条件，可以在保留掩码模型强大文本-运动生成先验的同时，实现高精度、灵活且可零样本泛化的时空控制。这一思路贯穿于训练和推理两个阶段的三个关键机制。

### 控制机制：从连续条件到 Logits 空间操纵

现有可控运动生成方法（如 **GMD** (Karunratanakul et al., ICCV 2023)、**OmniControl** (Xie et al., 2023)、**MotionLCM** (Luo et al., 2024)）大多基于扩散模型，在连续运动空间或潜在空间施加条件信号，而 **TLControl** (Wan et al., 2023) 则采用前馈 Transformer 加测试时优化。这些方法面临的核心瓶颈是：高精度关节控制与高质量运动生成难以兼得，且生成速度较慢（Table 1）。不可控的掩码运动模型 **MoMask** (Guo et al., 2023) 虽能快速生成高质量运动，但完全缺乏空间控制能力。

MaskControl 的解决方案是引入 **Logits Regularizer**——一个预训练掩码运动模型的可训练副本，通过零初始化的线性层与原始模型各 Transformer 层连接（Fig. 2(c), Sec. 3.2）。该模块接收关节控制信号 S，将其投影并注入 token 序列，从而**隐式扰动文本条件 logits**，使运动 token 的类别分布向控制信号对齐。这一设计使得控制信号通过 logits 空间的“软引导”发挥作用，而非在运动空间硬性约束，从而在保持生成质量的同时实现精确控制。

### 训练损失：从单一掩码重建到双目标约束

基线掩码模型 **MoMask** 仅使用掩码重建损失 $\mathcal{L}_{\mathrm{mask}}$（Eq. 2）进行训练，即仅基于文本条件预测被掩码的 token。MaskControl 在此基础上引入两个互补的损失函数，构成加权组合（Eq. 5）：

$$
\mathcal{L} = \alpha \mathcal{L}_{\mathrm{logits}} + (1 - \alpha) L_{s}(e_{c}, s)
$$

其中 **Logits Consistency Loss** $\mathcal{L}_{\mathrm{logits}}$（Eq. 4）将负对数似然扩展到所有位置（包括未掩码位置），条件同时包含文本 W 和关节控制信号 S，迫使 Logits Regularizer 在整个序列上学习控制信号到 token 分布的映射。**Motion Consistency Loss** $L_{s}(e_{c}, s)$（Eq. 3）则直接度量生成运动与输入控制信号之间的加权 L1 距离，通过运动学链解码器将 token 解码为全局 3D 关节位置后计算。两个损失的协同作用使模型既能学习控制信号的条件分布，又能显式优化控制精度。

### 推理采样：从标准重采样到梯度驱动的 Logits 优化

标准掩码模型的推理过程仅进行掩码预测与重采样，无法在推理时灵活响应新的控制需求。MaskControl 引入 **Logits Optimization**（Sec. 3.3），在推理时的解掩码过程中，通过梯度下降直接优化 logits 以最小化运动一致性损失：

$$
l_{m+1} = l_{m} - \eta \nabla_{l_{m}} L_{s}(l_{m}, s)
$$

这使得模型能在推理时根据任意目标函数调整生成结果，实现零样本目标控制（如约束人物在方形区域内行走，Table 4）。为支持这一梯度优化，MaskControl 设计了 **Differentiable Expectation Sampling (DES)**（Sec. 3.4, Fig. 2(b)），通过 Gumbel-Softmax（Eq. 9）将离散 token 采样转化为可微操作，并以码本向量的期望值 $\mathbb{E}[X_{recon}] = \sum_{k=1}^{K} p_{\theta}(x_k \mid \dots) \cdot c_k$ 作为连续嵌入，使梯度能流过离散量化过程。这一设计是连接离散 token 空间与连续运动控制的关键桥梁。

### 创新总结

MaskControl 的三个 changed slots 共同构成了一个完整的控制范式：**训练时**通过 Logits Regularizer 隐式学习控制信号到 token 分布的对齐，**推理时**通过 Logits Optimization 显式优化 logits 以精确跟随控制目标，**DES** 则保证整个流程的可微性。消融实验（Table 5）证实了这一设计的必要性：去除 Logits Regularizer 后 FID 从 0.061 升至 0.142，生成质量显著下降，验证了 logits 空间扰动对保持运动质量的关键作用。

MaskControl 的整体目标是在预训练的掩码运动模型（Masked Motion Model）之上引入可控性，使文本到运动生成能够同时满足高精度关节控制与高保真运动质量。其核心思路并非在连续运动空间直接施加条件，而是通过操控掩码 Transformer 输出的 **logits 分布**（即离散运动 token 的分类概率）来间接引导生成结果，从而在保留强大文本-运动先验的前提下实现灵活控制。

### 模块组成与数据流

系统由以下关键模块串联构成，其完整架构如图 2 所示：

1. **运动分词器（Motion Tokenizer）**  
   一个预训练的 VQ-VAE，负责将原始运动序列 $\mathbf{X}$ 压缩为离散的运动 token 序列。训练目标为标准向量量化损失：
   $$L_{VQ} = \| \operatorname{sg}(\mathbf{z}) - \mathbf{c_j} \|_2^2 + \beta \| \mathbf{z} - \operatorname{sg}(\mathbf{c_j}) \|_2^2$$
   该模块将连续运动映射到码本空间，为后续离散生成提供基础。

2. **文本条件掩码 Transformer（Text-conditioned Masked Transformer）**  
   预训练的核心生成器，以文本描述 $W$ 和部分可见的 token $X_{\overline{\mathbf{M}}}$ 为输入，预测被掩码位置的 token 分布。其原始训练目标为掩码重建损失：
   $$\mathcal{L}_{\mathrm{mask}} = - \underset{\mathbf{X} \in \mathcal{D}}{\mathbb{E}} \left[ \sum_{\forall i \in [1, L]} \log p \left( x_i \mid X_{\overline{\mathbf{M}}}, W \right) \right]$$
   该模块提供了强大的文本到运动生成先验，但本身不具备空间控制能力。

3. **Logits Regularizer（可训练副本）**  
   这是 MaskControl 在训练阶段引入的核心控制模块。它是一个与预训练掩码 Transformer 结构相同的可训练副本，两者通过零初始化的线性层逐层连接。Logits Regularizer 接收关节控制信号 $S$（指定哪些关节在哪些帧应处于何种位置），并将其投影后注入 token 序列，最终输出经过调节的 logits。其作用可理解为：**在不破坏原始文本条件分布的前提下，隐式地扰动 logits，使采样出的运动 token 趋向于满足控制信号**。

4. **运动学链解码器（Kinematic Chain Decoder）**  
   由解码器 $D$ 和运动学链函数 $R$ 组成。$D$ 将运动 token 解码回局部姿态表示，$R$ 则通过正向运动学将局部姿态转换为全局 3D 关节位置。这一模块使得模型可以在 3D 空间中对控制信号进行监督。

5. **可微期望采样（Differentiable Expectation Sampling, DES）**  
   推理时，从 logits 到离散 token 的采样过程原本是不可微的。DES 通过 Gumbel-Softmax 技巧将 logits 转换为 soft 概率分布，再计算码本向量的期望作为连续表示：
   $$\mathbb{E}[X_{recon}] = \sum_{k=1}^{K} p_{\theta} \left( x_{k} \mid X_{\overline{\mathbf{M}}}, W, S \right) \cdot c_{k}$$
   这使得梯度可以流经离散化步骤，是实现推理时优化的关键使能技术。

6. **Logits Optimization（推理时优化）**  
   在推理的去掩码过程中，模型以当前 logits 为优化变量，通过梯度下降最小化运动一致性损失 $L_s(e_c, s)$（即生成关节位置与控制信号之间的加权 L1 误差）：
   $$l_{m+1} = l_{m} - \eta \nabla_{l_{m}} L_s(l_{m}, s)$$
   优化后的 logits 被送回掩码 Transformer 进行重新预测，从而在保持生成分布的同时精确跟随控制目标。

### 训练与推理流程

**训练阶段**，模型同时优化两个目标：Logits Consistency Loss（在所有位置上基于文本和控制信号预测 token 的负对数似然）和 Motion Consistency Loss（解码后的全局关节位置与控制信号的加权 L1 误差），总损失为二者的加权组合：
$$\mathcal{L} = \alpha \mathcal{L}_{\mathrm{logits}} + (1 - \alpha) L_s(e_c, s)$$

**推理阶段**，模型执行迭代去掩码过程。在每个去掩码步骤中，Logits Optimization 对当前 logits 进行梯度优化以精确匹配控制信号，随后通过 DES 生成连续 token 表示，再经解码器重建运动。这一设计使 MaskControl 能够支持三种应用范式：任意关节任意帧控制、身体部位时间轴编辑，以及零样本目标函数控制——后者完全无需针对新控制目标重新训练，仅需在推理时定义相应的损失函数即可。

![[assets/figures/papers/storymotion_maskcontrol_iccv2025_20260603/figures/003_Figure_2.jpg]]
*Figure 2: Overall architecture of MaskControl. (a) Motion Tokenizer transforms the motion sequence into discrete motion tokens. (b) Differentiable Expectation Sampling (DES) is a differentiable sampling from logits enabling differentiable conversion between discrete tokens in codebook space and transformer token space. (c) Training: Logits Regularizer ensures high-quality motion by generating embedding closely aligns with joint control signals during an unmasking process. (d) Inference: Logits Optimization guides logits during the unmasking process at inference time based on the objective function*

### 3.1 运动离散化与掩码文本生成基座

MaskControl 建立在预训练的掩码运动模型之上，首先通过 **Motion Tokenizer（预训练 VQ-VAE）** 将连续运动序列离散化为 token。其核心损失为向量量化损失：

$$L_{VQ} = \| \operatorname{sg}(\mathbf{z}) - \mathbf{c_j} \|_2^2 + \beta \| \mathbf{z} - \operatorname{sg}(\mathbf{c_j}) \|_2^2 \quad \text{(Eq.1)}$$

其中 $\mathbf{z}$ 为编码器输出，$\mathbf{c_j}$ 为码本中选中的嵌入向量，$\operatorname{sg}(\cdot)$ 表示停止梯度算子。该损失使码本学习到运动空间的离散表示。

基于离散 token，**Text-conditioned Masked Transformer（预训练，冻结）** 以文本 $W$ 为条件，通过掩码预测范式生成运动 token。其训练目标为掩码重建损失：

$$\mathcal{L}_{\mathrm{mask}} = - \underset{\mathbf{X} \in \mathcal{D}}{\mathbb{E}} \left[ \sum_{\forall i \in [1, L]} \log p \left( x_i \mid X_{\overline{\mathbf{M}}}, W \right) \right] \quad \text{(Eq.2)}$$

其中 $X_{\overline{\mathbf{M}}}$ 表示未被掩码的 token 序列，$L$ 为序列长度。该损失仅基于文本条件，使模型学习到强大的文本-运动生成先验，但完全不具备空间控制能力。

### 3.2 Logits Regularizer：训练时隐式扰动

MaskControl 的核心创新在于通过操控 token 分类器的 logits 分布实现控制，而非直接在连续运动空间添加条件。**Logits Regularizer** 是实现这一目标的关键训练模块。

**结构设计**：Logits Regularizer 是预训练掩码 Transformer 的可训练副本，通过零初始化的线性层与原始模型逐层连接（Figure 2(c)）。其输入为 **Joint Control Signal Projection**——将控制信号 $S$（指定关节在特定帧的目标位置）投影并加到 token 序列上。

**双损失驱动**：Logits Regularizer 通过两个互补损失进行训练：

**(1) Motion Consistency Loss（运动一致性损失）**：衡量生成运动与输入控制信号之间的空间对齐程度：

$$L_{s}(e_{c}, s) = \frac{\sum_{n} \sum_{j} \sigma_{n j} \odot \lVert s_{n j} - R(D(e_{c})) \rVert}{\sum_{n} \sum_{j} \sigma_{n j}} \quad \text{(Eq.3)}$$

其中 $e_c$ 为 Logits Regularizer 输出的嵌入，$D$ 为解码器，$R$ 为运动学链解码器（将 token 解码为全局 3D 关节位置），$s_{nj}$ 为第 $n$ 帧第 $j$ 个关节的控制信号，$\sigma_{nj}$ 为二值控制指示符（有控制信号的关节/帧为 1，否则为 0）。该损失仅在受控关节和帧上计算加权 L1 距离。

**(2) Logits Consistency Loss（Logits 一致性损失）**：将掩码模型的负对数似然扩展到所有位置（包括未掩码位置），同时以文本和控制信号为条件：

$$\mathcal{L}_{\mathrm{logits}} = - \sum_{\forall i \in [1, L]} \log p \left( x_i \mid X_{\overline{\mathbf{M}}}, W, S \right) \quad \text{(Eq.4)}$$

该损失确保 Logits Regularizer 的输出 logits 在整个序列上与预训练模型的 token 分布保持一致，从而保留文本-运动生成先验。

**总训练损失**为两者的加权组合：

$$\mathcal{L} = \alpha \mathcal{L}_{\mathrm{logits}} + (1 - \alpha) L_{s}(e_{c}, s) \quad \text{(Eq.5)}$$

其中 $\alpha$ 平衡分布保持与控制精度。消融实验（Table 5）证实，去除 Logits Regularizer 会导致 FID 从 0.061 升至 0.142，证明该模块对保持生成质量至关重要。

### 3.3 Logits Optimization：推理时显式优化

训练完成后，Logits Regularizer 提供了控制信号到 logits 的隐式映射。为进一步提升控制精度，MaskControl 在推理时引入 **Logits Optimization**——通过梯度下降显式优化 logits 以最小化运动一致性损失。

**优化目标**：寻找使运动一致性损失最小的最优 logits $l^+$：

$$l^{+} = \arg \min_{l} \left( L_{s}(e_{c}, s) \right) \quad \text{(Eq.6)}$$

**更新规则**：在每次去掩码迭代中，对 logits 执行梯度下降：

$$l_{m+1} = l_{m} - \eta \nabla_{l_{m}} L_{s}(l_{m}, s) \quad \text{(Eq.7)}$$

其中 $\eta$ 为步长，$m$ 为优化迭代索引。Logits Optimization 在去掩码过程中扰动 logits，使掩码 Transformer 能够重新预测 token，从而在保持生成分布的同时精确跟随控制信号。

论文同时探索了在码本嵌入空间直接优化的替代方案：

$$e_{m+1} = e_{m} - \eta \nabla_{e_{m}} L_{s}(e_{m}, s) \quad \text{(Eq.8)}$$

但 logits 空间优化被证明更有效，因为它在 Transformer 的 token 预测层面操作，与预训练先验更兼容。

### 3.4 Differentiable Expectation Sampling (DES)：可微期望采样

Logits Optimization 需要梯度从运动一致性损失流回 logits，但离散 token 采样操作不可微。**Differentiable Expectation Sampling (DES)** 通过 Gumbel-Softmax 重参数化和期望值计算解决这一问题。

**Gumbel-Softmax 采样**：将 logits 映射到 token 概率分布：

$$p_{\theta} \left( x_{k} \mid X_{\overline{\mathbf{M}}}, W, S \right) = \frac{\exp \left( (\ell_{k} + g_{k}) / \tau \right)}{\sum_{j=1}^{K} \exp \left( \ell_{j} + g_{j} / \tau \right)} \quad \text{(Eq.9)}$$

其中 $g_k \sim \text{Gumbel}(0,1)$，$\tau$ 为温度参数，$K$ 为码本大小。

**期望重建**：不直接使用采样得到的离散 token，而是计算码本嵌入的加权期望：

$$\mathbb{E}[X_{recon}] = \sum_{k=1}^{K} p_{\theta} \left( x_{k} \mid X_{\overline{\mathbf{M}}}, W, S \right) \cdot c_{k}$$

其中 $c_k$ 为码本中第 $k$ 个嵌入向量。该期望值作为连续表示送入运动学链解码器 $R \circ D$，使梯度能够通过概率分布传播，绕过 argmax 量化的不可微性（Figure 2(b)）。在零样本目标控制等应用中，这一机制使任意可微目标函数的梯度都能影响 token 选择。

## 实验与关键发现

### 核心瓶颈与因果机制回顾

现有可控运动生成方法面临一个根本性权衡：基于扩散模型的方法（如 **GMD** (Karunratanakul et al., ICCV 2023)、**OmniControl** (Xie et al., 2023)、**MotionLCM** (Luo et al., 2024)）虽能实现一定程度的关节控制，但生成速度慢且运动质量（FID）受损严重；而基于掩码运动模型的方法（如 **MoMask** (Guo et al., 2023)）虽能高效生成高质量运动，却完全缺乏空间控制能力。**TLControl** (Wan et al., 2023) 通过前馈 Transformer 加测试时优化实现了较高控制精度，但 FID 高达 0.271，表明其生成质量显著下降。

MaskControl 的核心因果机制在于：**不直接在连续运动空间添加条件**，而是通过操纵掩码 Transformer 的 logits 分布来引导生成。具体而言，训练时引入 **Logits Regularizer**（预训练掩码模型的可训练副本，通过零初始化线性层连接）隐式扰动 logits，使其与关节控制信号对齐；推理时通过 **Logits Optimization** 对 logits 进行梯度下降优化，最小化运动一致性损失。这一设计使得模型既能保持掩码模型强大的文本到运动生成先验，又能实现高精度控制。

### 主要定量结果

#### 任意关节任意帧控制（Table 2）

![[assets/figures/papers/storymotion_maskcontrol_iccv2025_20260603/figures/006_Table_2.jpg]]
*Table 2: Comparison of text-condition motion generation with joint control signal on the HumanML3D. The first section, “Train on Pelvis Only,” evaluates our model that was trained solely on the pelvis. The last section, “Train on All Joints”, is trained on all joints and reports the average evaluation for each joint. → indicates the closer to the real value, the better*

在 HumanML3D 数据集上，MaskControl 在运动质量和控制精度两个维度上均显著超越现有方法。

**仅骨盆训练设置（Train on Pelvis Only）**：
- FID 从 TLControl 的 0.271 降至 **0.061**，降幅达 77%；相比 OmniControl 的 0.218 同样优势显著。
- 平均误差从 TLControl 的 1.08 cm 降至 **0.91 cm**。
- R-Precision Top-3 从 0.779 提升至 **0.809**，表明文本-运动语义一致性更好。
- 轨迹误差（>50cm）降至 **0.00%**，意味着生成的运动完全不会偏离控制轨迹超过 50 cm，而 TLControl 和 OmniControl 均存在此类严重偏离。

**全关节训练设置（Train on All Joints）**：
- 在所有关节上的平均 FID 为 **0.083**，远低于 TLControl（0.256）和 OmniControl（0.310）。
- 平均误差为 **0.91 cm**，同样优于对比方法。
- 这表明 MaskControl 在多关节控制场景下仍能保持生成质量，而扩散方法的质量退化更为严重。

#### 上身编辑任务（Table 3）

![[assets/figures/papers/storymotion_maskcontrol_iccv2025_20260603/figures/007_Table_3.jpg]]
*Table 3: Quantitative result of upper body editing task on HumanML3D dataset*

在上身编辑任务中，MaskControl 无需重新训练即可直接应用全关节训练模型：
- FID 为 **0.074**，优于 **MMM** 的 0.103 和 OmniControl 的 1.213。
- OmniControl 在此任务上 FID 高达 1.213，说明基于扩散的方法在编辑场景下运动质量急剧恶化，而 MaskControl 的 logits 操作范式在此类零样本迁移任务上具有天然优势。

#### 零样本目标控制（Table 4）

![[assets/figures/papers/storymotion_maskcontrol_iccv2025_20260603/figures/008_Table_4.jpg]]
*Table 4: Comparison of zero-shot objective control. Three Human-Scene Interaction objectives are adopted from the programmable motion model (ProgMoGen [30]). Both ProgMoGen and MaskControl are able to control motion during inference by arbitrary loss functions, while MDM and MoMask serve as uncontrollable baseline models*

MaskControl 的 Logits Optimization 机制天然支持推理时引入任意目标函数，无需针对特定控制目标重新训练。在三个 Human-Scene Interaction（HSI）任务上，与同样支持零样本目标控制的 **ProgMoGen** (Liu et al., CVPR 2024) 对比：

- **HSI-1（头部高度约束）**：约束误差为 **0.000**，实现零误差，优于 ProgMoGen 的 0.012。
- **HSI-2（避障）和 HSI-3（方形区域内行走）**：约束误差均显著低于 ProgMoGen。
- 不可控基线 **MDM** (Tevet et al., 2022) 和 MoMask 在这些任务上误差很大，验证了控制机制的必要性。

这组实验证明，Logits Optimization 在零样本目标控制上不仅可行，且精度优于专门设计的可编程运动模型 ProgMoGen。

### 消融实验（Table 5）

![[assets/figures/papers/storymotion_maskcontrol_iccv2025_20260603/figures/009_Table_5.jpg]]
*Table 5: Ablation results of components analysis and different densities of joint control signal*

消融实验系统验证了各模块的贡献：

**模块消融**：
- 完整模型：FID = 0.061，Avg Error = 0.98 cm。
- **去除 Logits Regularizer**：FID 升至 **0.142**（增加 133%），而误差几乎不变。这证明 Logits Regularizer 是保持生成质量的关键——仅靠推理时优化无法弥补训练阶段缺失的 logits 分布对齐。
- 去除 DES（可微期望采样）：FID 升至 0.147，误差升至 1.52 cm，表明可微采样对于梯度有效传导至关重要。
- 将 Logits Optimization 替换为 Embedding Optimization（Eq. 8）：FID 升至 0.108，误差升至 1.12 cm，说明在 logits 空间优化比直接在嵌入空间优化更有效，因为 logits 空间保留了 Transformer 的预测分布信息。

**控制密度分析**：
- 控制关节密度从 1 个关节增加到 100% 关节时，FID 有所改善（从 0.092 降至 0.061），但平均误差从 **0.10 cm 升至 1.64 cm**。
- 这揭示了一个精度-质量的权衡：密集控制信号会限制生成自由度，虽有助于维持整体运动分布（FID 改善），但模型难以精确满足所有关节的约束，导致局部误差累积。

### 定性结果（Figure 3, Figure 4）

![[assets/figures/papers/storymotion_maskcontrol_iccv2025_20260603/figures/004_Figure_3.jpg]]
*Figure 3: Visualization comparisons to state-of-the-art methods for any-joint any-frame control. The plots on the top display the top view of pelvis control (root trajectory), while the bottom plot shows the side view of the right wrist. Red represents the control signal, and Blue represents the generated joint motion*

- **Figure 3** 展示了任意关节任意帧控制的定性对比。在骨盆轨迹（俯视图）和右腕轨迹（侧视图）上，MaskControl 生成的蓝色曲线与红色控制信号几乎完美重合，而 TLControl 和 OmniControl 存在明显偏离。
- **Figure 4** 展示了零样本目标控制（方形区域内行走）的定性对比。MaskControl 生成的人物运动始终保持在方形边界内，而 ProgMoGen 出现越界情况。

### 失败模式与局限性

1. **密集控制退化**：当所有关节均提供控制信号时（100% 密度），平均误差从 0.10 cm 升至 1.64 cm，表明细粒度密集控制仍是挑战。模型在自由度被完全约束时难以同时满足所有关节的精确位置要求。
2. **量化表示限制**：方法基于 VQ-VAE 的离散 token 表示，可能丢失细微运动细节（如手指动作、微小的关节抖动）。
3. **推理计算开销**：Logits Optimization 需要梯度迭代，引入了额外计算成本。论文未报告推理时间对比，但梯度下降迭代（Eq. 7）必然增加延迟。
4. **应用范围受限**：当前仅针对单人运动生成，不支持多人交互或人与场景的复杂物理交互。

### 待验证与开放问题

- 推理优化步数 $m$ 和学习率 $\eta$ 对速度-精度 Pareto 前沿的影响未定量分析。
- 控制信号密度如何自适应选择以平衡精度和质量，尚无自动化策略。
- 在更大规模多模态数据集（如结合场景几何信息）上训练是否能进一步提升零样本控制能力，有待验证。
- 生成运动的物理合理性（如足部滑动、关节角度限制）缺乏定量评估指标。

## 定位与知识库关联

### 可控运动生成的范式演进

可控文本到运动生成领域可划分为三条主要技术路线：基于扩散模型、基于前馈模型、以及基于掩码模型。MaskControl 属于第三条路线，其核心创新在于首次为掩码运动模型引入了通用的时空控制能力。

**扩散模型路线**以 **MDM**（Tevet et al., 2022）为代表，通过扩散过程生成运动，随后 **GMD**（Karunratanakul et al., ICCV 2023）引入根关节轨迹控制，**OmniControl**（Xie et al., 2023）基于 ControlNet 架构将控制扩展至任意关节和任意时间点，**MotionLCM**（Luo et al., 2024）则转向潜在空间扩散以加速推理。这些方法的共同瓶颈在于：扩散采样固有的多步迭代导致生成速度较慢，且在追求高精度控制时往往牺牲运动质量（FID 升高）。

**前馈模型路线**以 **TLControl**（Wan et al., 2023）为典型代表，采用 Transformer 前馈网络结合测试时优化（Test-Time Optimization），实现了高精度关节控制。然而，该方法的代价是生成质量显著下降——在 HumanML3D 上的 FID 高达 0.271，远高于不可控的掩码模型 MoMask（FID 约 0.04）。这表明单纯在连续运动空间施加控制约束会破坏生成先验。

**掩码模型路线**以 **MoMask**（Guo et al., 2023）为基座，利用离散运动 token 和掩码预测范式实现了高质量的文本到运动生成，但完全缺乏空间控制能力。MaskControl 正是填补了这一空白：通过 Logits Regularizer 和 Logits Optimization 在离散 token 分布层面施加控制，而非在连续运动空间硬性约束，从而保留了掩码模型的强生成先验。

**零样本目标控制**方面，**ProgMoGen**（Liu et al., CVPR 2024）是唯一支持推理时任意目标函数控制的可编程运动生成方法。MaskControl 同样具备这一能力，且在三个 HSI 任务上均取得更优的约束误差，尤其在 Head Height Constraint 上实现零误差（Table 4），体现了 logits 层面优化相较于嵌入空间优化的优势。

### 核心机制差异：Logits 操作 vs. 连续空间条件

MaskControl 与现有可控运动生成方法的本质区别在于“在哪里施加控制信号”：

| 方法 | 控制施加位置 | 机制 | 质量-精度权衡 |
|------|-------------|------|--------------|
| GMD / OmniControl | 连续运动空间 | 扩散条件注入 / ControlNet | 精度提升伴随 FID 升高 |
| TLControl | 连续运动空间 | 前馈预测 + 测试时优化 | 高精度但 FID 极差（0.271） |
| **MaskControl** | **离散 token logits 分布** | **Logits Regularizer + Logits Optimization** | **FID 0.061 同时误差 0.91 cm** |

这一差异的因果机制在于：掩码模型将运动序列量化为离散 token，其生成过程本质上是基于文本条件的 token 分布预测。Logits Regularizer 通过一个可训练的复制网络（trainable copy），以零初始化线性层连接的方式，隐式地扰动预训练文本到运动模型的输出 logits，使 token 分布向控制信号对齐。这相当于在“概率空间”而非“几何空间”施加约束，因此不会破坏文本条件与运动 token 之间的统计依赖关系。

推理阶段的 Logits Optimization 进一步强化了这一范式：通过梯度下降直接优化 logits 以最小化运动一致性损失 $L_{s}(e_{c}, s)$，更新规则为 $l_{m+1} = l_{m} - \eta \nabla_{l_{m}} L_{s}(l_{m}, s)$。由于优化对象是 logits 而非运动参数，掩码 Transformer 可以在每次迭代中重新预测 token，使运动保持在“合理分布”附近。

### 可微期望采样（DES）的桥梁作用

离散 token 的不可微性是 logits 优化的关键障碍。MaskControl 通过 Gumbel-Softmax 重参数化实现可微采样：

$$p_{\theta} \left( x_{k} \mid X_{\overline{\mathbf{M}}}, W, S \right) = \frac{\exp \left( (\ell_{k} + g_{k}) / \tau \right)}{\sum_{j=1}^{K} \exp \left( \ell_{j} + g_{j} / \tau \right)}$$

随后以概率加权期望值 $\mathbb{E}[X_{recon}] = \sum_{k=1}^{K} p_{\theta} \cdot c_{k}$ 替代硬量化，使梯度能通过离散瓶颈反向传播。这一设计使得 Logits Optimization 的梯度更新能够直接影响连续运动重建，形成了“离散 logits → 连续期望嵌入 → 运动解码 → 控制损失”的可微链路。

### 适用边界与局限

**控制密度与精度的权衡**。消融实验（Table 5）揭示了控制信号密度对性能的非单调影响：当控制关节从 1 个增加到 100% 时，FID 有所改善（生成质量提升），但平均误差从 0.10 cm 急剧升至 1.64 cm。这表明密集的全关节控制对模型构成了过强约束，Logits Regularizer 和 Logits Optimization 的调节能力在极端密度下趋于饱和。当前方法缺乏自适应选择控制密度的机制。

**量化表示的固有局限**。MaskControl 依赖预训练的 VQ-VAE 将运动序列离散化为 token，这一压缩过程可能丢失细微的运动细节（如手指动作、面部表情）。在需要高保真度运动细节的场景（如手语生成、精细操作），量化误差可能成为瓶颈。

**推理计算开销**。Logits Optimization 需要 $I$ 次梯度迭代（原文未明确给出默认步数），每次迭代涉及前向传播和反向传播，引入了额外的推理时间成本。对于实时交互应用，需要探索优化步数与精度的 Pareto 前沿。

**场景限制**。当前方法仅针对单人运动生成设计，不支持多人交互、人物-物体交互等复杂场景。控制信号仅包含关节位置约束，不涉及物理合理性（如接触力、平衡约束）。

### 开放问题

1. **自适应控制密度选择**：能否根据文本语义或控制信号自动确定最优的控制关节密度，以动态平衡生成质量与控制精度？

2. **跨模态泛化**：Logits Regularizer + Logits Optimization 的范式是否可推广到其他离散生成任务？例如，在图像生成（VQGAN token）、音频生成（SoundStream token）中，是否同样可以通过扰动 logits 实现零样本控制？

3. **物理合理性评估**：当前评估仅依赖运动学指标（FID、平均误差），缺乏对生成运动物理合理性（如足部滑动、关节角度限制）的定量评估。如何设计标准化的物理合理性指标？

4. **大规模预训练的潜力**：在更大规模、多模态数据集（如结合视频、语言描述）上预训练掩码运动模型，是否能进一步提升零样本目标控制的泛化能力和精度？

5. **优化步数的效率前沿**：Logits Optimization 的迭代步数 $I$ 与最终控制精度和推理速度之间的关系如何？是否存在早停策略或自适应步长机制？

6. **多人交互扩展**：如何将 MaskControl 的时空控制框架扩展至多人场景？多人交互涉及空间协调和时序同步，对控制信号的表示和优化提出了更高要求。

## 原文 PDF

![[paperPDFs/ICCV_2025/MaskControl_Spatio_Temporal_Control_for_Masked_Motion_Synthesis.pdf]]

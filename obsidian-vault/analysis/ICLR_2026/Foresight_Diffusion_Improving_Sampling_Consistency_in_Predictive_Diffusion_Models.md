---
title: "Foresight Diffusion: Improving Sampling Consistency in Predictive Diffusion Models"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Foresight_Diffusion_Improving_Sampling_Consistency_in_Predictive_Diffusion_Models.pdf
aliases:
- FDF
- FDISCPDM
tags:
- ICLR_2026
- topic/generative_models_diffusion
- topic/generative_models_diffusion/generative_models_and_autoencoders
core_operator: "将条件理解从去噪过程中解耦，引入独立的确定性预测流，并使用预训练预测器进行两阶段训练。"
primary_logic: "通过架构分离和两阶段训练，解耦条件建模与去噪过程，可以显著提升预测扩散模型的预测准确性和采样一致性。"
claims:
- "与标准扩散模型相比，ForeDiff 在 RoboNet 上将 STD_LPIPS 从 0.65 降低到 0.35，表明采样一致性显著提升。"
- "ForeDiff 在 RT-1 上将 PSNR 从 30.4 提升到 31.2，同时将 STD_LPIPS 从 0.53 降低到 0.17。"
- "仅通过训练方案解耦（t=1 预训练）而不进行架构分离，无法达到 ForeDiff 的性能水平，证实架构分离的必要性。"
- "二阶段训练是保证预测表征稳定并有效支持去噪的唯一方案，联合训练只能提供有限增益且会损害生成质量或一致性。"
---

# Foresight Diffusion: Improving Sampling Consistency in Predictive Diffusion Models

> [!tip] 核心洞察
> 通过架构分离和两阶段训练，解耦条件建模与去噪过程，可以显著提升预测扩散模型的预测准确性和采样一致性。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | Foresight Diffusion：改善预测扩散模型的采样一致性 |
| 英文题名 | Foresight Diffusion: Improving Sampling Consistency in Predictive Diffusion Models |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=9WJoD0iDig) |
| Topic | #topic/generative_models_diffusion #topic/generative_models_diffusion/generative_models_and_autoencoders |
| Method | Foresight Diffusion (ForeDiff) |
| Dataset | RoboNet, RT-1 |

> [!tip] 效果简介
> - RoboNet 上，FVD↓ 为 51.5，对比 53.8 (Vanilla Diffusion)，变化 -2.3。
> - RoboNet 上，LPIPS↓ 为 5.25，对比 5.65，变化 -0.40。
> - RoboNet 上，STD_LPIPS↓ 为 0.35，对比 0.65，变化 -0.30。

## 概述

现有预测扩散模型在共享架构中联合处理条件输入与噪声目标，同质化的参数共享与单一的端到端训练使条件理解与目标去噪两个功能彼此纠缠。这一耦合造成两方面的代价：模型在纯噪声输入下的确定性预测能力远低于专用预测器，且跨多次采样的生成结果方差过大、最差情况下质量急剧退化，即存在**预测能力受限**与**采样不一致**的双重瓶颈（Figure 3, Section 3.2）。

Foresight Diffusion（ForeDiff）通过**架构与训练的双重解耦**应对上述问题：在结构上引入独立的确定性预测流（ViT block）处理条件，与生成流（DiT block）物理分离，仅通过轻量融合模块（AdaLN+MLP）传递条件表示；在训练上采用两阶段范式，先预训练预测流使其获得稳定的条件表征，再冻结该表征并仅训练生成流进行去噪。这一设计使模型能够专注于条件建模而不受去噪任务干扰，从而同时提升预测准确性和采样一致性（Figure 4, Section 3.3）。

实证结果支撑了这一核心洞察：在RoboNet视频预测上，ForeDiff相较标准扩散模型将FVD从53.8降至51.5，更关键的是将反映采样一致性的STD_LPIPS从0.65减至0.35；在RT-1上，PSNR提升0.8 dB（30.4→31.2），STD_LPIPS从0.53降至0.17（Table 1）。消融实验进一步验证，仅进行训练解耦（t=1预训练）而不拆开架构，不仅无法带来收益，甚至可能恶化FVD（Table 10）；联合训练虽能给出有限改进，但无法稳定预测表征并最终收敛至折中状态，失去扩散模型的生成优势（Table 11）；而移除确定性预测头、直接使用预测流中间表示，反而获得更优性能，表明富有信息的预测表示而非最终预测输出才是关键（Table 7）。此外，将相同参数规模的扩展原生扩散模型与ForeDiff进行公平对比，结果确认性能提升源自架构解耦本身而非参数数量（Table 9）。

综上所述，ForeDiff以简洁的架构分离和两阶段训练，在保持生成多样性的同时显著改善了预测扩散模型的确定性与采样一致性，为后续预测生成任务提供了一种新的范式。其效果在多个规模和场景下均具有高置信度，但更大规模模型与跨架构泛化性仍待进一步验证。

## 背景与动机

扩散模型凭借出色的生成能力，在视频预测、科学计算等需要学习未来联合分布的预测任务中展现出巨大潜力。标准做法是将条件输入（如历史帧、环境信号）与带噪目标一同送入条件去噪网络，通过协同优化来学习条件分布。然而，这种耦合设计在预测场景下暴露出两个根本性缺陷：**采样不一致**与**预测能力受限**。

如图1所示，在相同条件下，标准扩散模型（Vanilla Diffusion）生成的样本 LPIPS 分布宽而右偏，远不如确定性模型集中，表明其引入了大量不受条件控制的随机方差。进一步的诊断分析（Figure 3）揭示了这一现象的两条因果链：首先，在纯噪声输入（t=1）的条件下，标准扩散模型的预测精度显著低于一个纯确定性预测器，说明网络并未从条件中提取到足够强的语义以支撑准确预测；其次，尽管该模型在平均生成质量（FVD）上与基线持平乃至更优，但其「最差样本」误差突出，STD 指标（如 STD_LPIPS 达 0.65）远超可接受水平，意味着模型对部分条件根本无法给出可靠一致的输出。

这些后果的根源是**条件理解与目标降噪在共享架构与协同训练中的深度纠缠**。同组参数既要承担从噪声中恢复目标的「反向推理」，又要负责从条件中解析环境的「正向推理」。在联合优化中，去噪损失的随机性会持续干扰条件表示的稳定性，使网络无法形成专精于预测的确定性中间表征；反过来，条件表示的模糊又迫使去噪过程在分布的多种可能模式间随机跳跃，导致采样方差高企。简单的调参或增加容量只能实现生成质量与一致性之间的折衷，无法解开这一结构性矛盾。

因此，要使预测扩散模型同时具备高预测准确性与采样一致性，关键在于**将条件理解从去噪过程中解耦**。基于这一动机，本文提出 Foresight Diffusion (ForeDiff)：通过引入独立的确定性预测流，将条件建模移出噪声路径，并采用“先预测、后生成”的两阶段训练范式——先让预测流习得高质量确定性表示，再以其冻干表征引导生成流去噪。解耦后，条件表示不再受去噪扰动，生成流得以在稳定语义约束下采样，从而在保持生成多样性的同时，将采样一致性指标的方差大幅压缩（如 RoboNet 上 STD_LPIPS 从 0.65 降至 0.35），预测准确度亦明显提升（PSNR 从 30.4 升至 31.2）。该方案为预测扩散模型的架构设计提供了新的思考路径。

## 核心创新

**瓶颈与因果靶点**  
标准条件扩散模型（Vanilla Diffusion）将条件理解与目标去噪置于共享架构中联合训练，导致两个子任务的目标相互纠缠：模型要么牺牲预测精度以维持生成多样性，要么在确定性预测与随机降噪之间折中而失效。这一纠缠直接表现为采样不一致——同一条件输入的不同样本之间误差方差过高（RoboNet 上 STD_LPIPS 达 0.65），且预测能力显著弱于独立训练的同规模确定性模型（Figure 3c）。Foresight Diffusion（ForeDiff）的因果靶点正是**解耦条件建模与去噪过程**，通过架构分离和两阶段训练消除两者的互扰，从而同时提升预测准确度和采样一致性。

**架构创新：独立的确定性预测流**  
ForeDiff 将模型拆分为**预测流**（ViT 块）和**生成流**（DiT 块），分别处理条件输入 $\mathbf{y}$ 与带噪目标 $\mathbf{x}_t$（Figure 4c）。与之对比，普通扩散模型将 $\mathbf{y}$ 和 $\mathbf{x}_t$ 拼接后直接送入统一的 DiT 块（Figure 4a）。分离式架构赋予条件理解独立的前向通路：
$$
\mathbf{g}_0 = \mathrm{PatchEmbed}(\mathbf{y}), \quad \mathbf{g}_i = \mathrm{ViT}_i(\mathbf{g}_{i-1}),\ i=1,\dots,M,
$$
$$
\mathbf{h}_0 = \mathrm{PatchEmbed}(\mathbf{x}_t), \quad \mathbf{h}_1 = \mathrm{Fusion}(\mathbf{h}_0, \mathbf{g}_M, t).
$$
预测流产生的表示 $\mathbf{g}_M$ 通过轻量级融合模块（AdaLN + MLP）注入生成流（Eq. 6, Appendix B），避免条件信息被噪声掩盖。这一设计使条件理解完全不受噪声干扰，从结构上切断了此前两个任务的冲突（Table 10 证实：仅对普通模型做训练解耦而不做架构分离，性能远不及 ForeDiff）。

**训练创新：两阶段预测‑去噪解耦**  
架构分离仅为能力提供潜力，若沿用端到端联合训练，预测与生成两个损失仍会抢控共享的表示（Table 11 显示联合训练仅能带来微弱增益且损害生成质量或一致性）。ForeDiff 将训练分为两个阶段（Figure 4d, Eq. 7）：

1. **预训练预测器**：仅使用确定性损失训练预测流和一个临时预测头（PredHead），使 ViT 块学习到充分捕捉条件语义的表示；
2. **冻结表示训练生成流**：丢弃 PredHead，固定预测流的全部参数，仅训练生成流与融合模块，以预测流提供的稳定表示作为去噪的条件输入。

这一策略保证了**预测表示的质量与稳定性**，使得生成流可以“信任”注入的条件信号，而无需在去噪过程中重新学习条件理解。Table 12 进一步表明，即使预测器未完全收敛（0.5M 次迭代），ForeDiff 依然明显优于普通扩散模型，印证解耦训练对表示鲁棒性的宽容度。

**创新效果的因果证据**  
消融实验系统性地证实了解耦是增益的核心原因：① 仅扩展普通模型参数至相同规模无法匹配 ForeDiff（Table 9），改进来自架构设计而非参数量；② 两阶段解耦训练是唯一能充分利用确定性预测能力并保持扩散生成优势的方案（Table 11）；③ ForeDiff 在 RoboNet 上将 STD_LPIPS 从 0.65 降至 0.35，在 RT‑1 上从 0.53 降至 0.17（Table 1），说明采样一致性得到根本改善；④ PSNR、LPIPS 等均值指标同步提升，证明预测能力增强并非以生成多样性坍塌为代价（Table 13 的校准分析确认了概率建模的改进而非模式坍塌）。

综上，ForeDiff 的两个 changed slots——**架构分离**与**两阶段训练**——通过解耦条件理解与去噪的因果链路，系统性解决了预测扩散模型的核心缺陷，使模型在保持扩散生成灵活性的同时获得接近确定性预测器的精度与一致性。

## 整体框架

![[assets/figures/papers/iclr26_0013_9WJoD0iDig_Foresight_Diffusion_Improving_Sampling_Consisten/figures/006_Figure_4.jpg]]
*Figure 4: Overview of Foresight Diffusion. (a) Vanilla diffusion jointly processes condition and noisy target, limiting its predictive ability. (b) A Deterministic model focuses solely on condition understanding and achieves better predictive performance. (c) ForeDiff-zero introduces a separate predictive stream to isolate condition understanding from noise. (d) ForeDiff further adopts a twostage scheme: it pre-trains the predictive stream, then freezes its representations to guide generation*

Foresight Diffusion (ForeDiff) 的根本动机在于解决预测扩散模型的一个关键瓶颈：条件理解与目标去噪在共享架构和联合训练中相互纠缠，导致模型的预测能力受限、采样一致性差（Figure 3b, 3c）。为此，ForeDiff 引入了**双层解耦策略**——架构上的流分离与训练上的两阶段独立优化，将确定性预测与随机生成明确切割为两条不同的前向通路，从而在不牺牲生成多样性的前提下显著提升预测准确度与采样稳定性（Figure 2, 4）。

### 1 整体流水线：从原始视频到预测未来帧

整个框架的推理流程遵循典型的潜在扩散范式，并在此基础上构建分离的条件处理与去噪流水线。

**潜在空间压缩**  
原始视频帧首先通过预训练的自动编码器（Autoencoder，包含编码器 ℰ 与解码器 𝒟）压缩到低维潜在空间，以降低计算开销（Section 3.1）。后续所有的条件理解与去噪操作均在该潜在空间中完成。

**条件输入构造**  
条件输入 𝒚 由过去帧及环境信号（如机器人动作或物理参数）通过掩码策略（masking-based strategy）拼接得到，并用 Patch Embedding 转换为对预测流友好的 token 序列（Appendix B）。目标未来帧的潜在表示 𝒙₀ 在训练时通过前向加噪过程 𝒙ₜ = (1−t)𝒙₀ + t𝜖 生成带噪目标 𝒙ₜ（Eq. (1)）；在推理时，生成流从纯噪声开始逐步去噪。

### 2 架构解耦：ForeDiff-zero 骨干

ForeDiff-zero 将模型分为两条独立的信息流（Figure 4(c), Eq. (6)）：

- **预测流（Predictive Stream）**：由 M 个 ViT 块组成，仅处理条件输入 𝒚。其作用是**纯确定性**地从过去信息中提取对未来帧的预测性表示，不接触噪声目标，从而避免条件理解被去噪任务干扰。预测流输出为中间特征向量 𝙜_M。

- **生成流（Generative Stream）**：由多个 DiT 块构成，专门处理带噪目标 𝒙ₜ。其输入为噪声目标的 Patch Embedding 𝙝₀。为将预测流的知识注入生成过程，设计了一个轻量级**融合模块（Fusion Module）**，该模块由自适应层归一化（AdaLN）和双层 MLP 组成，操作形式为  

  𝙝₁ = MLP( AdaLN( [ 𝙝₀ ; 𝙜_M ], t ) )  

  (Appendix B)。融合后的特征 𝙝₁ 再经后续 DiT 块进行去噪，最终输出预测的速度场 𝒗_θ(𝒙ₜ, t, 𝒚) 或去噪后的数据。

### 3 训练解耦：两阶段学习

仅靠架构分离（ForeDiff-zero）并不能直接带来采样一致性的显著改善（Table 1 中 ForeDiff-zero 的 STD_LPIPS 与普通扩散模型相近），这表明还需要在训练过程中明确挖掘预测流的确定性表征能力。ForeDiff 引入了两阶段训练（Figure 4(d), Eq. (7)）：

1. **第一阶段（确定性预训练）**：在预测流末端附加一个小的预测头（PredHead），用真实未来帧 𝒙₀ 作为监督信号，最小化 L₂ 损失 ℒ_determ，将该流训练成纯粹的确定性预测器。此时生成流不参与训练。
2. **第二阶段（生成流训练）**：丢弃 PredHead，冻结预测流的全部参数，仅用去噪损失 ℒ_denoise 训练生成流和融合模块。此时预测流提供的已是富含预测信息的稳定中间表示，而非最终的预测值，实验表明这种表示远比显式预测输出更有益（Table 7，移除 PredHead 后指标明显提升）。

联合训练（即同时优化两部分）会迫使模型在预测与生成间折衷，无法同时稳定两个目标（Table 11）；而仅对普通扩散模型进行 t=1 预训练微调而不进行架构分离，也无法达到 ForeDiff 的性能水平（Table 10），证实了**架构解耦与训练解耦缺一不可**。

### 4 推理时的信息流

推理阶段，条件 𝒚 首先经过冻结的预测流得到确定性表示 𝙜_M。然后，从纯噪声 𝒙₁ 开始，在每一时间步将 𝒙ₜ 与 𝙜_M 送入融合模块后，由生成流预测当前速度场，再通过反向积分得到下一时刻的潜在 𝒙_{t−Δt}（Eq. (3)）。最终，解码器 𝒟 将去噪后的潜在表示还原为预测的未来视频帧。由于条件建模完全被隔离在预测流中，生成流在去噪过程中不再需要对条件进行复杂理解，采样一致性由此得到根本保障。

## 核心模块与公式推导

### 整体框架与模块拆解
ForeDiff 围绕“条件理解与去噪解耦”这一核心洞察，构造了四个关键模块：

- **自动编码器（Encoder/Decoder）**：将视频帧压缩到低维潜在空间，降低计算开销。
- **确定性预测流（Predictive Stream）**：由多级 ViT 块组成，独立处理条件输入（过去帧、环境信号），输出富含预测信息的隐表示 `g_M`。
- **生成流（Generative Stream）**：基于 DiT 块的去噪网络，接收噪声目标 `x_t` 并将预测表示通过融合模块注入，完成从噪声到未来帧的生成。
- **融合模块（Fusion Module）**：采用自适应层归一化（AdaLN）加两层 MLP，将预测流输出 `g_M` 与噪声目标 `h_0` 拼接，并注入扩散时间步 `t`，形成两条流的交互接口。
- **预测头（PredHead）**：只在第一阶段训练的临时模块，将预测流输出映射为确定性未来帧；第二阶段训练时被移除。

### 关键公式

#### 1. 前向扩散过程的线性插值
```math
\mathbf{x}_t = (1 - t) \mathbf{x}_0 + t \epsilon, \quad t \in [0, 1]
```
- `x_0`：原始未来帧的潜在表示。
- `ε ~ N(0, I)`：标准高斯噪声。
- `t`：扩散时间步，`t=0` 对应干净数据，`t=1` 对应纯噪声。

#### 2. 条件速度场学习目标
```math
\mathcal{L}_{\mathrm{velocity}}(\theta) := \mathbb{E}_{\mathbf{x}_0, \epsilon, t}\left[\| \mathbf{v}_{\theta}(\mathbf{x}_t, t, \mathbf{y}) - (\epsilon - \mathbf{x}_0) \|^2\right]
```
- `v_θ`：参数化的速度场，预测从当前状态到目标的变化方向。
- `y`：条件输入（掩码过去帧及控制信号）。
- 该损失驱动模型学会在任意 `t` 下从 `x_t` 向 `x_0` 方向“流动”。

#### 3. 纯噪声条件下的预测能力诊断
```math
\mathcal{L}_{\mathrm{pred}}(\theta|t=1) = \mathbb{E}_{\mathbf{x}_0, \mathbf{y}, \epsilon}\left[\|\hat{\mathbf{x}}_{\theta}(\epsilon, 1, \mathbf{y}) - \mathbf{x}_0\|_2^2\right]
```
- `x̂_θ(ε, 1, y)`：在输入为纯噪声 `ε`（`t=1`）时，模型对原始数据 `x_0` 的预测。
- 该度量被证明存在偏差‑方差下界，暴露普通条件扩散模型预测能力受限的本质。

#### 4. 确定性预测器损失
```math
\mathcal{L}_{\mathrm{deter}}(\xi) = \mathbb{E}_{\mathbf{x}_0, \mathbf{y}}\left[\|f_{\xi}(\mathbf{y}) - \mathbf{x}_0\|_2^2\right]
```
- `f_ξ`：纯确定性模型，直接从条件 `y` 映射到目标 `x_0`。
- 此损失用于第一阶段预训练预测流，为其提供强大的条件建模能力。

#### 5. ForeDiff-zero 架构方程
```math
\begin{aligned}
\mathbf{g}_0 &= \mathrm{PatchEmbed}(\mathbf{y}), \quad \mathbf{g}_i = \mathrm{ViT}_i(\mathbf{g}_{i-1}), \; i=1,\ldots,M,\\
\mathbf{h}_0 &= \mathrm{PatchEmbed}(\mathbf{x}_t), \quad \mathbf{h}_1 = \mathrm{Fusion}(\mathbf{h}_0, \mathbf{g}_M, t), \quad \mathbf{h}_{i+1} = \mathrm{DiT}_i(\mathbf{h}_i, t)
\end{aligned}
```
- `g_i`：预测流第 `i` 个 ViT 块的输出；`M` 为 ViT 块总数。
- `h_i`：生成流第 `i` 个 DiT 块的输出。
- `Fusion(·)`：融合模块，其内部运算为 `h_1 = MLP(AdaLN([h_0; g_M], t))`，将噪声目标、预测表示和时间步进行拼接与自适应归一化。

该架构实现了条件的确定性理解与噪声的去噪生成完全分离，是 ForeDiff 的骨干。

#### 6. 两阶段训练损失函数
**第一阶段**——确定性预训练：
```math
\mathcal{L}_{\mathrm{determ}} = \mathbb{E}_{\mathbf{x}_0, \mathbf{y}}\left[\|P_{\xi}(\mathbf{y}) - \mathbf{x}_0\|_2^2\right]
```
**第二阶段**——生成流去噪训练（预测流冻结）：
```math
\mathcal{L}_{\mathrm{denoise}} = \mathbb{E}_{\mathbf{x}_0, \mathbf{y}, \epsilon, t}\left[\|G_{\theta}(\mathbf{x}_t, P_{\xi}'(\mathbf{y}), t) - (\epsilon - \mathbf{x}_0)\|_2^2\right]
```
- `P_ξ`：带预测头的第一阶段模型；`P_ξ'` 表示移除预测头后保留的冻结预测流输出。
- `G_θ`：以冻结的预测特征 `P_ξ'(y)` 和时间步 `t` 为条件的生成流。
- 两阶段设计确保预测表征稳定，再去学习去噪映射，显著提升采样一致性。

## 实验与分析

本节在真实机器人视频预测（RoboNet、RT‑1）和科学预报（HeterNS）三个场景中评估Foresight Diffusion（ForeDiff），重点回答三个问题：(1) 主结果是否在准确性与采样一致性上显著优于扩散基线及确定性预测器；(2) 架构解耦与两阶段训练各自贡献多大；(3) 一致性收益是否以模式坍塌为代价。所有数据均源自原文的定量表与消融图，必要时标注需要手动验证的细节。

### 主结果：视频预测与科学预报

**机器人视频预测**（Table 1）。在RoboNet上，ForeDiff将FVD从53.8降至51.5，LPIPS从5.65降至5.25，同时将采样一致性的关键指标STD LPIPS从0.65压至0.35，降幅约46%。在RT‑1上，PSNR由30.4提升至31.2，STD LPIPS则由0.53降至0.17，降幅达68%。图1的LPIPS核密度估计显示，ForeDiff的预测分布更窄且均值更低，明显优于传统扩散模型和iVideoGPT自回归基线。定性可视化（图5、图6）进一步印证：普通扩散模型中粉红铲子扭曲、玩具物件崩溃，RT‑1中机器人位置和背景亮度预测失准，而ForeDiff输出结构更合理、时序更稳定。

![[assets/figures/papers/iclr26_0013_9WJoD0iDig_Foresight_Diffusion_Improving_Sampling_Consisten/figures/007_Table_1.jpg]]
*Table 1: Robot video prediction results on RoboNet and RT-1 datasets. SSIM and LPIPS scores are scaled by 100 for convenient display*

![[assets/figures/papers/iclr26_0013_9WJoD0iDig_Foresight_Diffusion_Improving_Sampling_Consisten/figures/001_Figure_1.jpg]]
*Figure 1: Kernel density estimation: LPIPS distributions of generated samples. Shaded areas represent estimated probability densities; dashed lines indicate sample means. A lower LPIPS corresponds to better quality*

值得注意的是，仅做架构分离而未引入两阶段预训练的ForeDiff‑zero（Table 1）在STD指标上与普通扩散无显著差异，说明**冻结的预测表示而非架构分离本身驱动了采样一致性的质变**。

**科学预报**（Table 4/Table 9）。在HeterNS数据集上，普通扩散模型的Relative L2高达1.50，确定性预测器约为0.95，而ForeDiff将该指标降至0.18，误差大幅缩小。该场景下对精确物理量预测的需求极高，ForeDiff的优势尤其突出。

![[assets/figures/papers/iclr26_0013_9WJoD0iDig_Foresight_Diffusion_Improving_Sampling_Consisten/figures/021_Table_9.jpg]]
*Table 9: ForeDiff clearly outperforms both deterministic-only and extended vanilla diffusion models, confirming that its improvements stem from architectural design rather than model size alone. Metrics are scaled by 100*

### 消融分析

**预测头（PredHead）的作用**。移除PredHead（即在第一阶段的预测输出头）后，在所有数据集上感知与像素指标均进一步改善（Table 7），说明生成流直接利用预测流的**中间表示**，而非最终确定性输出，对去噪更有利。

**预测流容量**。固定生成流为12个DiT块时，增加预测流ViT块数M从0至9可提升性能，继续增至12则收益递减（Table 8）。这种“适度增加有益、过度增加饱和”的模式在两个数据集上一致，表明将一部分计算量分配给条件理解比堆叠同等规模的扩散主干更有效。

**架构解耦 vs. 训练解耦**（Table 10）。将普通扩散模型仅进行训练解耦（即在t=1预训练，再在所有时间步微调，架构不变）无法达到ForeDiff的水平。结果明确表明：**架构分离是获得稳定一致性提升的必要条件**，单独的训练策略改动不足以消除条件与去噪任务之间的互扰。

![[assets/figures/papers/iclr26_0013_9WJoD0iDig_Foresight_Diffusion_Improving_Sampling_Consisten/figures/022_Table_10.jpg]]
*Table 10: Necessity of architectural decoupling. Results comparing (1) Vanilla Diffusion, (2) Vanilla Diffusion with training-only decoupling (pretraining at t = 1 followed by fine-tuning across timesteps), and (3) ForeDiff with both training- and architectural decoupling*

**二阶段训练的必要性**（Table 11）。联合训练（同时优化预测损失和去噪损失）虽可带来微弱增益，但最终收敛到性能折衷点，生成质量或一致性难以兼顾。二阶段方案（先冻结预测表示，再训练生成流）是唯一能在保持扩散生成能力的同时充分利用确定性前馈信息的策略。

![[assets/figures/papers/iclr26_0013_9WJoD0iDig_Foresight_Diffusion_Improving_Sampling_Consisten/figures/023_Table_11.jpg]]
*Table 11: Necessity of two-stage training. While joint training can offer mild gains, it ultimately converges to a compromised middle ground. The two-stage decoupled design of ForeDiff remains the most effective and stable solution for leveraging deterministic foresight while preserving diffusion’s generative strengths*

**参数规模 vs. 架构设计**（Table 9 与图8(c)）。在同等参数总量下，扩大的普通扩散模型和纯确定性预测器均远逊于ForeDiff，证明**性能增益源自架构分离而非单纯增加参数**。图8(c)的散点对比直观体现了这一结论。

**预训练质量敏感性**（Table 12）。ForeDiff对预测流预训练的收敛程度不敏感：即使仅用0.5M次迭代的未完全收敛预测器，最终模型仍获得显著提升。这表明两阶段设计无需强依赖一个高精度确定性预测器，降低了对第一阶段训练的要求。

### 校准与一致性验证

**覆盖校准**（Table 13，图9）。为了验证一致性提升是否来自简单丢弃随机性（即模式坍塌），作者进行了覆盖度校准评估。结果显示ForeDiff在预测区间覆盖精度和样本‑分布相似性两方面均优于基线，说明模型既提高了单次预测的可靠性，又未退化为单一确定性模式，概率建模更加合理。

### 失败模式与局限

1. **规模验证缺失**：所有实验受限于学术计算资源，未在百亿参数级模型或超大规模数据集上验证。解耦思路本身与缩放定律正交，但其在大规模下的实际收益仍需要系统性研究（原文开放问题）。
2. **骨干架构依赖**：当前实验完全基于DiT骨干，虽然解耦设计原则上可迁移至CNN或混合架构，但此类扩展尚无实验证据。
3. **范式局限**：研究范围限定在扩散模型内部，将条件理解与去噪解耦的核心理念能否泛化到自回归、能量模型等其他生成范式，尚未探索。
4. **预测器训练细节**：默认1.0M次迭代的预测器可能存在轻微过拟合，更精细的早停或正则化策略能否带来跨数据集一致的进一步增强，仍有待验证。

以上局限性均需对照实际场景进行手动确认，尤其是当迁移到不同数据分布、规模或架构时，现有结论并非不经实验即可推广。

## 方法谱系与知识库定位

### 与基线工作的关系

ForeDiff 直接对标的是**预测扩散模型**中的两类基线：**标准条件扩散模型**（Vanilla Diffusion）和**纯确定性预测器**。文章通过诊断实验（Figure 3）揭示了标准扩散模型的核心矛盾：它在感知质量（FVD）上表现高效，但采样一致性差——在 RoboNet 上最佳与平均 LPIPS 尚可，最差情况却显著恶化（Figure 3b），且其纯预测能力逊于一个简单的确定性模型（Figure 3c）。这一矛盾源于条件特征理解与目标去噪在共享架构中的纠缠（见 Lemma 1 证明，附录 A），而 ForeDiff 通过**架构分离**和**训练解耦**打破了该纠缠。

与 Vanilla Diffusion 相比，ForeDiff 将模型拆分为两条流：预测流（ViT 块）处理条件输入，生成流（DiT 块）基于噪声目标去噪，两者通过轻量级融合模块（AdaLN + MLP）连接。这一架构改变使 ForeDiff 在 RoboNet 上将 STD_LPIPS 从 0.65 降至 0.35，在 RT-1 上进一步从 0.53 降至 0.17（Table 1），同时 FVD 和 PSNR 也有相应改善。更重要的是，消融实验明确表明，仅靠训练方案调整（如 t=1 预训练后微调）而不进行架构解耦，无法达到 ForeDiff 的性能（Table 10）；联合训练也无法同时稳定预测与生成，最终收敛至折衷状态，而二阶段训练则是唯一有效利用确定性预测能力并保持扩散优势的方案（Table 11）。因此，ForeDiff 并非简单的多流设计，而是从因果机制上解决了条件建模与去噪过程互相干扰这一根本瓶颈。

与**iVideoGPT**（自回归视频预测基线）的对比主要集中在采样一致性的分布形态上（Figure 1）：扩散模型在多次采样中会产生较宽的 LPIPS 分布，代表生成多样性但预测精度不足；iVideoGPT 的分布则更集中但质量更低；ForeDiff 在保持感知质量的同时显著收窄了分布，实现了生成多样性与预测确定性之间的平衡（Figure 2）。在数值上，ForeDiff 未与 iVideoGPT 进行全指标对决，但其设计目标正是为了解决扩散模型在预测场景下的“过度随机性”问题。

与**确定性预测器**相比，ForeDiff 并未丢弃扩散生成的优势，而是利用预训练的确定性表示来引导去噪。消融显示，在同等参数规模下，ForeDiff 大幅优于扩展的确定性模型和扩展的 Vanilla Diffusion，证明改进来自架构设计而非参数数量（Table 9）。特别地，即便预测流未完全收敛（0.5M 次迭代），ForeDiff 仍能获得显著提升，显示其对预测器质量不敏感（Table 12）。此外，移除预测头（PredHead）后性能反升（Table 7），表明预测流提供的中间表示而非最终预测输出对生成更有益。

**ForeDiff-zero** 作为消融中间态（仅架构分离、联合训练）未在采样一致性上产生实质改善（Table 1），进一步凸显了两阶段训练的必要性：第一阶段将预测流训练为确定性预测器，第二阶段冻结其表示并指导生成流的去噪过程。这一设计构成了 ForeDiff 与所有共用架构基线在方法论上的核心区别。

### 适用边界与局限

ForeDiff 的设计前提是预测任务中存在**条件与目标之间的语义鸿沟**，且传统的联合建模会损害预测的稳定性和一致性。因此，该方法最适用于需要高采样一致性和可校准预测的场景，例如机器人视频预测（RoboNet、RT-1）和科学时空预报（HeterNS）。对于纯粹追求多样性的生成任务（如无条件图像生成），ForeDiff 的解耦不带来明显收益，因为不存在条件理解与生成纠缠的需求。同样，若条件与目标之间是简单的一对一映射，分开建模可能引入冗余开销。

文章自身指出的局限性有三：
1. **规模化验证缺失**：实验受限于学术计算资源，未在大型模型或大规模数据集上检验解耦设计的缩放特性。作者虽认为解耦思想与缩放定律正交，但其在大规模条件下的效益仍需系统研究。
2. **骨干架构局限**：当前实验均基于 DiT 骨干扩散模型，尽管解耦原则可推广至 CNN 或混合架构，但尚未获得验证。
3. **生成范式限制**：解耦条件理解与去噪的核心洞察虽可能泛化至自回归、能量模型等其他生成范式，但尚未探索。

此外，从消融中可推论：预测流的 ViT 块数量存在收益递减（Table 8），过度增加块数无益；预训练迭代次数（默认 1.0M）可能存在轻微过拟合，表 12 的敏感性测试未显示严重性能下降，但更精细的早停策略是否进一步提升尚未进一步研究。

### 开放问题与对后续工作的启发

ForeDiff 提出的“条件-去噪解耦”框架为预测生成模型带来新的研究方向：
- **规模化行为**：如何系统地将 ForeDiff 扩展到更大骨干网络和数据集，并量化其缩放规律？其与缩放定律的正交性需在更大规模上重新检验。
- **跨架构泛化**：解耦策略在 CNN 或 CNN/Transformer 混合架构的扩散模型上能否取得类似收益？不同骨干下的最优融合方式可能不同。
- **跨范式推广**：这一核心洞察（条件理解与生成去噪的分离）能否移植到自回归、流匹配或其他非扩散生成范式，从而改善这些模型在预测任务中的一致性？
- **训练精细度**：当前二阶段训练未严格优化第一阶段早停策略；更精细的预测器训练（如更早停止或正则化）是否会进一步提升下游生成性能，同时保持跨数据集的一致性？
- **校准与不确定性**：Table 13 和 Figure 9 展示了 ForeDiff 在覆盖校准上的优势，表明它避免了模式坍塌。进一步的研究可探索如何利用解耦框架显式建模认知不确定性与任意不确定性，使预测扩散模型更适合安全关键型应用。

总而言之，ForeDiff 在预测扩散模型的方法谱系中确立了一个新的定位：通过架构与训练双解耦，提升采样一致性的同时保持生成质量，为后续预测生成模型的设计提供了清晰的改进路径和验证基准。

## 原文 PDF

![[paperPDFs/ICLR_2026/Foresight_Diffusion_Improving_Sampling_Consistency_in_Predictive_Diffusion_Models.pdf]]

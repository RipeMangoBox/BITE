---
title: "PAS: A Training-Free Stabilizer for Temporal Encoding in Video LLMs"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/PAS_A_Training_Free_Stabilizer_for_Temporal_Encoding_in_Video_LLMs.pdf
project_link: null
code_link: "https://github.com/Bowen-Sun-0728/PAS"
aliases:
- PASP
- PAS
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: "在推理时对查询流(Q)施加按注意力头分组的小幅度、反向相位偏移(如K=2组,偏移量[0, 0.5] bin单位),使不同头在略微偏移的时滞处采样同一IFT调制波形,通过标准多头聚合实现受控移动平均,从而平滑有效调制。"
primary_logic: "将M-RoPE在时间轴上的注意力logit分解为内容点积⟨q,k⟩与IFT调制因子Re{m(∆)}的乘积(相位调制近似,定理1),揭示时间不稳定的根源在于调制核的非平滑性。PAS通过在不同注意力头上施加相位偏移并聚合,等效于在时域对m(t)进行短程移动平均,在频域通过聚合核K(ω)=∑a_h e^{jωαδ_h}衰减非零频率线的幅度(|K(ω)|<1),从而降低m(t)的高频波纹,提升注意力的Lipschitz稳定性(定理2-3),同时在各头满足Nyquist采样条件时保持每头频谱幅值不变(定理4)。"
claims:
- "RoPE-rotated attention logit can be approximated as the unrotated content dot product multiplied by a scalar IFT kernel Re{m(∆)}, isolating the temporal modulation from content si..."
- Smoother IFT kernel implies Lipschitz stability of attention to small temporal shifts, with the logit change bounded by the kernel's maximal local slope L_m.
- Multi-phase aggregation across heads with dispersed offsets provably reduces the mean-square local variation of the effective modulation, yielding a smoother waveform.
- Per-head temporal offsets preserve DFT magnitudes under Nyquist-band-limited sampling; PAS alters only how modulation is sampled and aggregated, not what each head encodes.
---

# PAS: A Training-Free Stabilizer for Temporal Encoding in Video LLMs

> [!tip] 核心洞察
> 将M-RoPE在时间轴上的注意力logit分解为内容点积⟨q,k⟩与IFT调制因子Re{m(∆)}的乘积(相位调制近似,定理1),揭示时间不稳定的根源在于调制核的非平滑性。PAS通过在不同注意力头上施加相位偏移并聚合,等效于在时域对m(t)进行短程移动平均,在频域通过聚合核K(ω)=∑a_h e^{jωαδ_h}衰减非零频率线的幅度(|K(ω)|<1),从而降低m(t)的高频波纹,提升注意力的Lipschitz稳定性(定理2-3),同时在各头满足Nyquist采样条件时保持每头频谱幅值不变(定理4)。

| 字段 | 内容 |
|------|------|
| 中文题名 | PAS: 视频大语言模型中时序编码的无训练稳定器 |
| 英文题名 | PAS: A Training-Free Stabilizer for Temporal Encoding in Video LLMs |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2511.10979) · [Code](https://github.com/Bowen-Sun-0728/PAS) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | Phase Aggregated Smoothing (PAS) |
| Dataset | 20BN-Jester, Something-Something V2, Kinetics-700, Breakfast Actions |

> [!tip] 效果简介
> - 20BN-Jester 上，Accuracy 18.3 (PAS) vs Default Setting (lower, see Table 1) (positive improvement)。
> - Something-Something V2 上，Accuracy 16.3 (PAS) vs Default Setting (lower, see Table 1) (positive improvement)。
> - Kinetics-700 上，Accuracy 48.2 (PAS) vs Default Setting (lower, see Table 1) (positive improvement)。

## 概要

视频大语言模型（Video LLM）通过时序位置编码将帧间时间关系注入注意力机制，使模型能够理解视频中的动态事件。然而，当前广泛采用的 **M-RoPE**（Multi-dimensional Rotary Position Embedding）沿时间轴引入了一个逆傅里叶变换（IFT）调制核 $m(\Delta)$，该核由有限离散频率线 $\{\omega_i\}$ 的余弦平均构成，在帧尺度上存在**固有的非平滑性（波纹）**。当关键帧恰好落入调制波形的低增益波谷时，其信息被抑制甚至忽略，注意力决策被偶然的时序偏移而非内容相似性主导（Figure 1）。这一瓶颈源于一个根本性的因果机制：**注意力 logit 可近似分解为内容点积与标量 IFT 调制因子 $\mathrm{Re}\{m(\Delta)\}$ 的乘积**（定理1），而 $m(\Delta)$ 的非平滑性直接决定了注意力对微小时间偏移的敏感度。

针对上述问题，本文提出 **PAS（Phase Aggregated Smoothing）**，一种**无需训练、即插即用的推理时稳定器**。其核心操作极为简洁：在推理时将注意力头划分为 $K$ 组（默认 $K=2$），对查询流 $\mathbf{Q}$ 施加按组区分的小幅度、反向相位偏移（如 $[0, 0.5]$ bin 单位），使不同头在略微偏移的时滞处采样同一 IFT 调制波形，随后通过标准多头聚合实现受控移动平均，从而平滑有效调制（Figure 2）。PAS 的理论支撑完整且自洽：

- **定理2** 证明注意力 logit 对时间偏移的变化被 $m(\Delta)$ 的最大局部斜率 $L_m$ 所约束——更平滑的调制意味着更稳定的注意力。
- **定理3** 证明多相位聚合后的有效调制 $m_{\text{eff}}(\Delta t) = \sum_h a_h m(\Delta t + \delta_h)$ 在均方局部变差上严格不超过原始调制，在频域通过聚合核 $K(\omega) = \sum a_h e^{j\omega \delta_h}$ 衰减非零频率线的幅度（$|K(\omega)| < 1$），从而降低高频波纹。
- **定理4** 证明在 Nyquist 带限条件下，每头时序偏移仅改变 DFT 相位，幅值保持不变——PAS 改变的是调制的采样和聚合方式，而非每头编码的频谱内容。

在方法谱系中，PAS 属于**推理时稳定化方法**，与 **SlowFast-LLaVA**（通过慢速/快速双路径稳定决策）和 **TS-LLaVA**（通过缩略图与轻量时序流混合扩展时间覆盖）等训练无关的 Video LLM 推理时基线形成互补——PAS 可透明叠加于这些方法之上，无需额外训练或输入修改。

实验覆盖九个基准（包括动作识别数据集 20BN-Jester、Something-Something V2、Kinetics-700、Breakfast Actions，以及通用视频 LLM 评测套件 MVBench、TempCompass、PerceptionTest、EgoSchema、MMBench-Video），在匹配 token 预算下，PAS 带来**一致且显著的准确率提升**（Table 1）。消融实验进一步验证了理论预测：偏移量在 0.3–0.8 范围内具有广泛平台效应（Figure 4），PAS 在低采样率下增益最大，随采样率增大逐渐收敛至与原始 backbone 统计不可区分（Figure 5）——这与定理2的预测一致，即密集采样本身已平滑了 IFT 核的有效探测。计算开销方面，PAS 的吞吐量（$76.8 \times 10^3$ tokens/s）与原始 backbone（$77.2 \times 10^3$ tokens/s）在统计上不可区分，理论开销比 $C_{\text{PAS}}/C_{\text{attn}} \leq p_t S_v / S^2$ 可忽略。

PAS 的局限性同样明确：当采样率足够高时增益趋于消失；在 Nyquist 欠采样场景下改进窗口更窄；仅适用于采用 M-RoPE 且具备独立时序维度编码的模型；当前默认设置虽表现良好，但偏移量的自适应学习策略仍有待探索。

### 视频LLM中的时序位置编码

视频大语言模型（Video LLM）的核心挑战之一是如何让模型感知帧之间的时序关系。与文本不同，视频信号天然具有时间维度，模型必须理解“动作的先后顺序”“事件的时间跨度”等时序信息才能正确回答诸如“他先拿起杯子还是先打开门”之类的问题。

当前主流Video LLM广泛采用**M-RoPE（Multi-dimensional Rotary Position Embedding）** 来编码时序位置信息。M-RoPE将RoPE的旋转位置编码机制从文本的一维序列扩展到多维空间，在时间轴上引入一组离散的频率线 $\{\omega_i\}$，通过旋转注意力中的查询向量 $\mathbf{q}$ 和键向量 $\mathbf{k}$，使得注意力logit仅依赖于查询与键之间的相对时间位移 $\Delta$：

$$\langle \tilde{\mathbf{q}}, \tilde{\mathbf{k}} \rangle (\Delta) = \mathrm{Re} \left[ \sum_{i=0}^{m-1} C_i e^{\mathrm{j} \omega_i \Delta} \right]$$

这一机制在理论上赋予了模型感知时序距离的能力，但也埋下了本文所揭示的核心隐患。

### 核心瓶颈：IFT调制核的非平滑性

M-RoPE在时间轴上的注意力logit可以分解为内容相似度与一个标量调制因子的乘积。具体而言，定义**IFT（逆傅里叶变换）调制核**：

$$m(\Delta) := \frac{1}{m} \sum_{i=0}^{m-1} e^{\mathrm{j} \omega_i \Delta}$$

在高维多线近似下（定理1），RoPE旋转后的注意力logit近似为：

$$\langle \tilde{\mathbf{q}}, \tilde{\mathbf{k}} \rangle (\Delta) \approx \langle \mathbf{q}, \mathbf{k} \rangle \cdot \mathrm{Re} \{ m(\Delta) \}$$

这一分解揭示了问题的本质：注意力决策被分解为**内容相关性**（$\langle \mathbf{q}, \mathbf{k} \rangle$）和**时序调制**（$\mathrm{Re}\{m(\Delta)\}$）两个独立因子的乘积。然而，$m(\Delta)$ 由有限个离散频率线的余弦平均构成，在帧尺度上存在**固有的非平滑波纹**——相邻帧的注意力会被乘以差异显著的调制因子。

**实际后果**：当关键帧恰好落入调制波形的低增益波谷时，其信息被抑制甚至忽略，注意力决策被偶然的时序偏移而非内容相似性主导。Figure 1展示了一个真实案例：由于时序RoPE引入了与帧间隔相关的增益调制，关键帧落入低增益波谷后被下权重，导致模型关注了语义上不相关的帧，最终传播为下游错误。

### 现有方法的缺口

针对Video LLM的时序稳定性问题，已有一些训练无关的推理时方法被提出：

- **SlowFast-LLaVA**：通过慢速（低FPS、高空间细节）和快速（高FPS、激进下采样）双路径来稳定决策，但本质上是改变输入采样策略，并未直接解决M-RoPE内部的调制非平滑性。
- **TS-LLaVA**：通过紧凑缩略图保留全局空间线索，并与轻量时序采样流混合以扩展时间覆盖，同样属于输入层面的策略。

这些方法都绕开了根本问题——它们修改的是“模型看到了哪些帧”，而非“模型如何对待不同帧之间的时序关系”。M-RoPE调制核的非平滑性依然存在，当关键帧恰好落入波谷时，模型仍然可能做出错误的注意力分配。

### 本文动机与核心洞察

本文的核心洞察是：**M-RoPE在时间轴上的不稳定性根源在于IFT调制核 $m(\Delta)$ 的非平滑性**。更平滑的调制核意味着更小的局部斜率 $L_m$，从而直接约束注意力对微小时间偏移的敏感度（定理2，Lipschitz稳定性界）：

$$\big| A(\Delta t + \delta t) - A(\Delta t) \big| \leq \big| \langle \mathbf{q}, \mathbf{k} \rangle \big| L_m |\delta t|$$

基于这一洞察，本文提出**Phase Aggregated Smoothing（PAS）**——一种训练无关、即插即用的推理时稳定器。其核心思想是：在推理时对查询流（Q）施加按注意力头分组的小幅度、反向相位偏移，使不同头在略微偏移的时滞处采样同一IFT调制波形，然后通过标准的多头聚合实现受控移动平均，从而平滑有效调制（Figure 2）。

PAS的优雅之处在于：它不改变token化、模型参数、视频帧数量或任何输入，仅修改查询流的时序相位；每个注意力头独立地保持其频谱幅值不变（定理4），平滑效应仅在多头聚合后自然产生；计算开销在统计上与原始backbone不可区分。

## 核心方法与创新机理

PAS的核心创新在于揭示了视频大语言模型中广泛使用的**M-RoPE（多分辨率旋转位置编码）沿时间轴存在一个此前未被指出的固有缺陷**，并针对该缺陷提出了一种**极轻量、无需训练、即插即用的推理时稳定机制**。

### 问题发现：M-RoPE时域调制的非平滑性

M-RoPE将时间维度编码为一组有限离散频率线{ω_i}的余弦平均。PAS通过**相位调制近似定理（Theorem 1）** 首次将RoPE旋转后的注意力logit分解为两个独立因子的乘积：

$$\langle \tilde{\mathbf{q}}, \tilde{\mathbf{k}} \rangle (\Delta) \approx \langle \mathbf{q}, \mathbf{k} \rangle \cdot \mathrm{Re} \{ m(\Delta) \}$$

其中⟨q,k⟩是内容相似度，而Re{m(∆)}是一个仅依赖相对时滞∆的**标量调制因子**。这一分解揭示了问题的本质：注意力决策同时受内容相似度和一个与内容无关的时域调制波形控制。

该调制核m(∆)由有限频率线的逆傅里叶变换（IFT）构成，在帧尺度上呈现出**固有的非平滑波纹**——相邻帧的注意力被乘以差异显著的调制因子。当关键帧恰好落入调制波形的低增益波谷时（如Figure 1所示），其信息被系统性抑制甚至忽略，注意力决策被**偶然的时序偏移而非内容相似性主导**。

### 解决方案：相位聚合平滑（PAS）

针对上述瓶颈，PAS的核心操作仅涉及**两个changed slots**：

**1. 查询流时序相位（从统一到分组偏移）**

- **Baseline**：所有注意力头使用相同的时间相位（δ=0），查询Q直接使用M-RoPE编码后的结果。
- **PAS**：将查询注意力头划分为K组（默认K=2），每组共享一个时序偏移φ_g（如[0, 0.5] bin单位），仅对查询流施加Γ_δ相位旋转。该操作仅作用于时序半维度，保持空间编码完整。

**2. 有效时域调制平滑度（从固有波纹到受控移动平均）**

- **Baseline**：原始IFT核m(t)在帧尺度上存在固有波纹，相邻帧的调制增益可能剧烈波动。
- **PAS**：经多头聚合后，有效调制变为各头在偏移时滞处采样的原始调制核的加权平均：

$$m_{\mathrm{eff}}(\Delta t) := \sum_{h=1}^{H} a_h m(\Delta t + \delta_h)$$

这等效于在时域对m(t)进行**短程移动平均**。在频域，聚合核K(ω)=∑a_h e^{jωδ_h}对非零频率线产生衰减（|K(ω)|<1），从而抑制高频波纹。

### 理论保障的三层递进逻辑

PAS的设计由四个定理构成严密的因果链：

- **Theorem 1（相位调制近似）**：将注意力logit分解为内容项与调制项的乘积，定位不稳定性根源为m(t)的非平滑性。
- **Theorem 2（Lipschitz稳定性界）**：证明注意力对微小时间偏移的敏感度被m(t)的最大局部斜率L_m所约束——更平滑的调制核意味着更稳定的注意力。
- **Theorem 3（变差不等式）**：严格证明多相位聚合后的有效调制在均方局部变差上不超过原始调制，且当偏移非全同时严格更平滑。
- **Theorem 4（每头频谱不变性）**：在Nyquist带限条件下，时序偏移仅改变每头观测序列的DFT相位，幅值保持不变——PAS改变的是调制的采样和聚合方式，而非每头编码的频谱内容。

### 与现有训练无关方法的本质区别

PAS与SlowFast-LLaVA、TS-LLaVA等训练无关基线处于不同的作用层面：后者通过修改视频token化策略（慢速/快速双路径、缩略图混合）来扩展时间覆盖，而PAS直接修正M-RoPE编码本身引入的注意力偏差。这使得PAS可以**透明地叠加**在这些方法之上，无需额外训练或输入修改，产生进一步的性能增益（Table 1中SlowFast+PAS与TS-LLaVA+PAS的堆叠结果验证了这一点）。

### 开销的可忽略性

PAS的每层计算开销与注意力开销之比为：

$$\frac{C_{\mathrm{PAS}}}{C_{\mathrm{attn}}} \leq \frac{S_v d_t}{S^2 d_h} = \frac{p_t S_v}{S^2}$$

由于时序维度占比p_t很小且序列长度S很大，该比值可忽略。实测吞吐量（原始backbone 77.2±3.1 ×10³ tokens/s vs PAS 76.8±4.0 ×10³ tokens/s）在统计上不可区分，证实改进并非以计算开销为代价。

PAS（Phase Aggregated Smoothing）是一个**训练无关、即插即用**的推理时稳定器，作用于视频大语言模型（Video LLM）中已部署M-RoPE的注意力层。其核心操作极为精简：在标准多头注意力的计算流程中，**仅对查询流（Q）施加按注意力头分组的小幅度时序相位偏移，随后依赖模型自身的标准多头聚合机制自然产生平滑效应**。整个pipeline不修改任何模型参数、token化策略、视频帧数量或输入表示。

### 输入输出流

PAS的输入是视频LLM在某一注意力层中已通过M-RoPE编码的查询张量Q。输出是经过相位旋转后的Q′，随后与未修改的键张量K和值张量V一同进入标准的多头注意力计算与聚合。具体而言：

- **输入**：查询张量 $Q \in \mathbb{R}^{H \times S_v \times d}$，其中 $H$ 为注意力头数，$S_v$ 为视觉token数，$d$ 为每头维度。该Q已完成M-RoPE的空间维度和时序维度的旋转编码。
- **输出**：相位旋转后的 $Q'$，仅其时序半维度被修改，空间编码保持完整不变。$Q'$ 随后与未经修改的K、V进行标准的缩放点积注意力计算，最终通过多头拼接与线性投影完成聚合。
- **关键约束**：PAS**仅作用于查询流**，键流和值流完全不受影响。这一设计确保了每头观测到的频谱幅值不变（定理4），平滑效应完全来源于多头聚合时的受控移动平均。

### 三阶段模块关系

PAS的完整pipeline可分解为三个串行模块，每个模块的功能边界清晰：

#### 1. 相位分组划分（Phase Group Partitioning）

将模型的 $H$ 个查询注意力头划分为 $K$ 个不相交的组 $\{G_g\}_{g=0}^{K-1}$。每组内的所有头共享同一个时序偏移量 $\varphi_g$。默认配置为 $K=2$，两组偏移量分别为 $\varphi_0 = 0$ 和 $\varphi_1 = 0.5$（以bin为单位）。分组策略决定了后续多头聚合时参与移动平均的采样点数量和分布。

#### 2. 逐头查询相位旋转（Per-Head Query Phase Rotation, $\Gamma_\delta$）

对每个查询头 $Q_h$（$h \in G_g$）施加时序相位旋转算子 $\Gamma_{\delta_h}$，其中 $\delta_h = \varphi_g$。该算子在频域等价于将查询的时序分量沿时间轴平移 $\delta_h$ 个bin单位，数学上实现为对查询向量的时序半维度乘以复指数相位因子。**空间半维度保持原样**，确保PAS不干扰模型对空间内容的编码能力。此操作的计算开销与注意力计算本身相比可忽略不计（开销比 $\leq p_t S_v / S^2$，其中 $p_t$ 为时序维度占比，$S$ 为序列总长）。

#### 3. 标准多头注意力与聚合（Standard Multi-Head Attention and Aggregation）

使用相位旋转后的 $Q'$ 与原始 $K$、$V$ 计算注意力权重和上下文向量，随后按标准流程进行多头拼接和线性投影。**平滑效应正是在这一聚合步骤中自然产生的**：由于不同头组在略微偏移的时滞处采样同一个IFT调制波形 $m(t)$，多头聚合等价于对 $m(t)$ 进行加权移动平均，得到有效调制 $m_{\text{eff}}(\Delta t) = \sum_h a_h m(\Delta t + \delta_h)$。频域分析表明，该聚合核 $K(\omega) = \sum_h a_h e^{j\omega \delta_h}$ 对非零频率线具有衰减作用（$|K(\omega)| < 1$ for $\omega \neq 0$），从而压制了原始调制波形的高频波纹，提升了注意力对微小时间偏移的Lipschitz稳定性。

### 与外部方法的叠加关系

PAS的即插即用特性使其可以**透明地叠加**在其他训练无关的Video LLM推理方法之上。例如，SlowFast-LLaVA和TS-LLaVA各自通过不同的采样策略构建视频token序列，PAS可在这些方法生成的token序列基础上直接施加相位偏移，无需修改预处理流程或增加额外训练。实验表明，PAS与这些方法的组合能带来进一步的性能提升（如20BN-Jester上SlowFast+PAS达到19.6%，TS-LLaVA+PAS达到19.3%，均优于各自单独使用）。

### 计算开销

PAS的理论计算开销与注意力计算之比为 $\frac{C_{\text{PAS}}}{C_{\text{attn}}} \leq \frac{S_v d_t}{S^2 d_h} = \frac{p_t S_v}{S^2}$。由于时序维度占比 $p_t$ 很小（通常为1/4或更小）且序列长度 $S$ 很大，该比值在实际部署中可忽略。实测吞吐量数据验证了这一点：原始backbone吞吐量为 $(77.2 \pm 3.1) \times 10^3$ tokens/s，PAS为 $(76.8 \pm 4.0) \times 10^3$ tokens/s，两者在统计上不可区分。

![[assets/figures/papers/paper_list_l2133_https_arxiv_org_abs_2511_10979/figures/002_Figure_2.jpg]]
*Figure 2: Temporal non-smoothness of the time domain modulation from original M-RoPE (upper) and how Phase Aggregated Smoothing (PAS) mitigates it (lower). PAS assigns small, opposed phase shifts to the query stream per head. Each head preserves its spectrum magnitude because a time shift only rotates phases. Head aggregation then acts as a controlled moving average in time, producing a smoother effective modulation across adjacent frames and reducing low gain induced suppression of key frames*

![[assets/figures/papers/paper_list_l2133_https_arxiv_org_abs_2511_10979/figures/003_Figure_3.jpg]]
*Figure 3: Implementation of PAS. For the*

### 问题形式化：M-RoPE 的时序非平滑性

PAS 的理论起点是对 M-RoPE 注意力机制的信号处理视角重构。给定查询向量 $\mathbf{q}$ 和键向量 $\mathbf{k}$，经 RoPE 旋转后的注意力 logit 仅依赖于二者的相对时间位移 $\Delta$，并可表达为频率线集合的加权复指数和的实部：

$$\langle \tilde{\mathbf{q}}, \tilde{\mathbf{k}} \rangle (\Delta) = \mathrm{Re} \left[ \sum_{i=0}^{m-1} C_i e^{\mathrm{j} \omega_i \Delta} \right]$$

其中 $C_i$ 为内容系数，$\{\omega_i\}_{i=0}^{m-1}$ 为 M-RoPE 分配的有限离散时间频率线。这一形式揭示了注意力 logit 的核心结构：它是内容相似度与位置调制的耦合产物。

**定理 1（相位调制近似）** 在标准的高维频率线假设下，上述 logit 可近似分解为未旋转的内容点积与标量逆傅里叶变换（IFT）调制核的乘积：

$$\langle \tilde{\mathbf{q}}, \tilde{\mathbf{k}} \rangle (\Delta) \approx \langle \mathbf{q}, \mathbf{k} \rangle \cdot \mathrm{Re} \{ m(\Delta) \}$$

其中 IFT 核定义为：

$$m(\Delta) := \frac{1}{m} \sum_{i=0}^{m-1} e^{\mathrm{j} \omega_i \Delta}$$

这一分解分离了内容贡献与位置贡献，直接揭示了瓶颈所在：$m(\Delta)$ 由有限离散频率线的余弦平均构成，在帧尺度上存在**固有波纹**——相邻帧的注意力被乘以差异显著的调制因子。当关键帧恰好落入调制波形的低增益波谷时，其信息被抑制甚至忽略，注意力决策被偶然的时序偏移而非内容相似性主导（见 Figure 1）。

![[assets/figures/papers/paper_list_l2133_https_arxiv_org_abs_2511_10979/figures/001_Figure_1.jpg]]
*Figure 1: A failure from a real clip [2]. Temporal RoPE imposes an interval-dependent gain on attention; when a key frame lies in a low-gain trough of the modulation, it is down weighted compared to less relevant frames, which propagates to downstream errors*

**定理 2（Lipschitz 稳定性界）** 注意力 logit 对微小时间偏移 $\delta t$ 的变化被 IFT 核的最大局部斜率 $L_m$ 所约束：

$$\big| A(\Delta t + \delta t) - A(\Delta t) \big| \leq \big| \langle \mathbf{q}, \mathbf{k} \rangle \big| L_m |\delta t|$$

$L_m$ 直接量化了时序不稳定的程度：$m(t)$ 的波纹越剧烈，$L_m$ 越大，注意力对时序抖动越敏感。这为 PAS 的设计提供了因果操纵柄——**平滑 $m(t)$ 即可降低 $L_m$，提升注意力稳定性**。

### 核心机制：多相位聚合平滑

PAS 的核心操作可分解为三个模块，均在推理时执行，不涉及任何训练或参数修改。

**模块 1：相位分组（Phase Group Partitioning）**

将查询流的所有注意力头划分为 $K$ 组 $\{G_g\}_{g=0}^{K-1}$，每组内所有头共享同一时序偏移量 $\varphi_g$。默认配置为 $K=2$，偏移量取 $[0, 0.5]$（以 bin 为单位），即一组头保持原始相位，另一组头施加半个频率 bin 的相位偏移。这一分组策略在频域上形成受控的采样点分散。

**模块 2：逐头查询相位旋转（Per-Head Query Phase Rotation $\Gamma_\delta$）**

对每组查询头 $Q_h$ 施加时序相位旋转 $\Gamma_{\delta_h}$，该操作**仅作用于时间半维度**，保持空间编码完全不变：

$$Q_h \leftarrow \Gamma_{\delta_h}(Q_h)$$

$\Gamma_\delta$ 的本质是对查询向量在时间子空间上施加一个与 $\delta$ 成正比的相位旋转。由于仅修改查询流，键流和值流保持不变，注意力计算仍为标准形式，但每个头在略微偏移的时滞处采样同一 IFT 调制波形。

**模块 3：标准多头聚合（Standard Multi-Head Aggregation）**

使用相位旋转后的 $Q$ 与未修改的 $K$、$V$ 计算注意力，随后按标准多头注意力机制进行拼接和投影。平滑效应在此聚合步骤**自然产生**，无需额外操作。聚合后的有效调制为各头采样的加权平均：

$$m_{\mathrm{eff}}(\Delta t) := \sum_{h=1}^{H} a_h m(\Delta t + \delta_h)$$

其中 $a_h$ 为各头的聚合权重（默认均匀分布）。这一操作在时域上等效于对原始调制核 $m(t)$ 进行短程移动平均，在频域上等效于通过聚合核 $K(\omega) = \sum a_h e^{\mathrm{j} \omega \delta_h}$ 衰减非零频率线的幅度（$|K(\omega)| < 1$ for $\omega \neq 0$），从而抑制 $m(t)$ 的高频波纹。

**定理 3（变差不等式）** 定义均方局部变差泛函：

$$\mathcal{V}_{\varepsilon}(f) := \lim_{T \to \infty} \frac{1}{T} \int_0^T (f(\tau + \varepsilon) - f(\tau))^2 d\tau$$

该泛函量化函数在滞后 $\varepsilon$ 上的平均平方差异，值越小表示波形越平滑。PAS 聚合后的有效调制满足：

$$\mathcal{V}_{\varepsilon}(m_{\mathrm{eff}}) \leq \mathcal{V}_{\varepsilon}(m)$$

当偏移量非全同且权重非零时，不等式严格成立。这从理论上保证了多相位聚合必然产生比原始调制更平滑的有效波形（见 Figure 2 的上下对比）。

**定理 4（每头频谱不变性）** 在 Nyquist 带限假设下，时序偏移 $\delta$ 仅改变每头观测序列的 DFT 相位，幅值保持不变：

$$X_{\delta}[k] = e^{\mathrm{j} \theta_k(\delta)} X[k] \Longrightarrow |X_{\delta}[k]| = |X[k]|$$

这意味着 PAS 改变的是调制核的**采样和聚合方式**，而非每头编码的频谱内容。各头保留了与 backbone 完全相同的频谱幅值信息，平滑效应纯粹来源于多头聚合时的相消干涉。

### 计算开销分析

PAS 每层的额外计算开销 $C_{\mathrm{PAS}}$ 与标准注意力开销 $C_{\mathrm{attn}}$ 之比为：

$$\frac{C_{\mathrm{PAS}}}{C_{\mathrm{attn}}} \leq \frac{S_v d_t}{S^2 d_h} = \frac{p_t S_v}{S^2}$$

其中 $S_v$ 为视频 token 数，$S$ 为总序列长度，$d_t$ 为时间半维度，$p_t$ 为时间维度占比。由于 $p_t$ 很小且 $S$ 很大，该比值在实践中可忽略。实验验证：原始 backbone 吞吐量为 $(77.2 \pm 3.1) \times 10^3$ tokens/s，PAS 为 $(76.8 \pm 4.0) \times 10^3$ tokens/s，两者在方差范围内统计不可区分。

## 实验与关键发现

### 主实验结果

PAS在九个基准测试上对基础Video LLM backbone产生了**一致的、正向的准确率提升**,所有对比均在匹配的token预算和完全相同的预处理/解码流程下进行。Table 1汇总了训练无关的匹配token结果。

在动作识别任务上,PAS在**20BN-Jester**上达到18.3%,在**Something-Something V2**上达到16.3%,在**Kinetics-700**上达到48.2%,均显著优于Default Setting backbone。在视频LLM通用基准上,PAS在**MVBench**上达到69.5%,在**TempCompass**上达到73.3%,在**PerceptionTest**上达到68.9%,在**EgoSchema**上达到63.9%,在**MMBench-Video**上达到1.78 Mean Score,全面超越原始backbone。

值得注意的是,PAS可以**透明地叠加**在其他训练无关的推理时方法之上。将PAS与SlowFast-LLaVA或TS-LLaVA堆叠后,在20BN-Jester上分别达到19.6%和19.3%,相比单独使用这些方法进一步提升了性能。这种可叠加性源于PAS仅修改查询流的时序相位,与这些方法修改输入帧采样策略的机制完全正交。

在**Breakfast Actions**数据集上,PAS的改进窗口更窄且绝对增益较小(45.3%)。该数据集的时序采样未满足M-RoPE频率线集合的Nyquist条件(见Table 2),混叠效应限制了有效收益——这与理论预测一致:当采样本身已经欠Nyquist时,对已混叠的IFT核进行平滑的空间有限。

### 消融实验

#### 偏移量扫描

Figure 4展示了固定K=2分组下,不同偏移量∆对四个数据集准确率的影响。在三个运动丰富的数据集——**20BN-Jester、Something-Something V2和Kinetics-700**——上,∆在**0.3到0.8 bin单位**范围内带来稳定且显著的增益,呈现广泛的平台效应。这一平台特性降低了参数敏感性和实际调优难度。推荐的默认值∆≈0.5恰好落在此平台的中心位置。

Breakfast Actions数据集由于欠Nyquist采样,改进窗口明显更窄,仅在∆的特定子区间内获得正向收益。这与Theorem 2的理论框架一致:当采样不满足Nyquist条件时,IFT核的有效探测已受混叠污染,相位偏移平滑的边际收益降低。

#### 采样率消融

Figure 5展示了固定K=2、∆=0.5条件下,不同采样率r对PAS效果的影响。PAS在**低采样率下增益最大**,随着采样率r增大,其准确率逐渐收敛至与原始backbone统计上不可区分的水平。

这一趋势与Theorem 2的理论预测精确吻合:密集采样本身已经提供了对IFT核的充分平滑探测——当帧间隔足够小时,m(t)在相邻采样点间的波纹已被自然平均化,推理时额外平滑的空间随之减小。换言之,PAS的增益与采样率呈反比关系,这从实验上验证了"IFT核非平滑性是时序不稳定根源"的核心论断。

#### 计算开销

吞吐量实测显示,原始backbone的吞吐量为**(77.2±3.1)×10³ tokens/s**,PAS为**(76.8±4.0)×10³ tokens/s**,两者在方差范围内统计不可区分。理论开销比由公式给出:

$$\frac{C_{\mathrm{PAS}}}{C_{\mathrm{attn}}} \leq \frac{S_v d_t}{S^2 d_h} = \frac{p_t S_v}{S^2}$$

由于时序维度占比$p_t$很小且序列长度$S$很大,PAS的每层计算开销相对于注意力计算本身可忽略。这一可忽略的开销源于PAS仅对查询流$Q$的时序半维度施加相位旋转($\Gamma_\delta$),不修改键流$K$、值流$V$或注意力矩阵的计算。

### 失败模式与局限

**高采样率下的增益消失**是PAS最明确的边界条件。当采样率足够高时,密集帧采样本身已实现了对IFT核的充分平滑探测,PAS的额外平滑效果趋于零。这不是方法的缺陷,而是其理论机制的必然推论——PAS解决的是稀疏采样下的调制波纹问题,当问题本身因密集采样而消失时,解决方案自然不再产生额外收益。

**欠Nyquist采样场景**构成另一类挑战。在Breakfast Actions数据集上,时序采样未满足M-RoPE频率线集合的Nyquist条件,导致改进窗口窄化且绝对增益有限。混叠效应使得原始调制波形已经失真,相位偏移平滑无法完全补偿频谱混叠带来的信息损失。

**空间主导任务**上PAS的改进可能有限。PAS仅作用于查询流的时序半维度,保持空间编码不变。对于主要依赖空间外观线索而非时序关系的任务(如静态场景识别),PAS的时序平滑机制不产生直接帮助。

**方法适用范围**受限于底层模型使用M-RoPE且具备独立时序维度编码。PAS不适用于其他位置编码方案(如绝对位置编码、学习式位置编码或标准的1D/2D RoPE)。

### 关键图表结论

**Figure 1**揭示的失败案例直接验证了核心瓶颈:当关键帧恰好落入M-RoPE调制波形$m(t)$的低增益波谷时,该帧的注意力被显著下权重,导致模型关注不相关的帧并产生下游错误。这种由偶然时序偏移而非内容相似性主导的注意力决策,正是PAS所要解决的根本问题。

**Figure 2**直观对比了原始M-RoPE与PAS的时域调制平滑度。原始调制(上图)在帧尺度上呈现明显的非平滑波纹,相邻帧间调制增益剧烈波动;PAS聚合后的有效调制(下图)通过受控移动平均显著平滑了波形,降低了关键帧被偶然抑制的风险。

**Figure 3**展示了PAS的简洁实现:仅对每个视觉token的$Q$矩阵施加逐头时序偏移,操作局限于查询流和时序维度,无需修改模型参数、token化流程或任何输入。

**Table 2**的Nyquist条件标注为理解各基准上的性能差异提供了关键背景。满足Nyquist条件的基准(如20BN-Jester、Kinetics-700)上PAS改进显著且稳定;欠Nyquist的基准(如Breakfast Actions)上改进受限——这从频域角度解释了失败模式的根本原因。

![[assets/figures/papers/paper_list_l2133_https_arxiv_org_abs_2511_10979/figures/004_Table_1.jpg]]
*Table 1: Training-free, matched-token results including stacked variants. PAS applies per-head offsets [0, 0.5] in bin units. Rows above the horizontal rule list the backbone and single-method baselines; rows below show PAS stacked with other methods. Color coding: blue marks the best score within the upper block (above the rule) for each metric column, and green marks the best score over the entire column*

![[assets/figures/papers/paper_list_l2133_https_arxiv_org_abs_2511_10979/figures/005_Table_2.jpg]]
*Table 2: Benchmarks used in our evaluation. The Nyquist column indicates whether the effective temporal sampling meets the Nyquist condition for the temporal RoPE line set*

![[assets/figures/papers/paper_list_l2133_https_arxiv_org_abs_2511_10979/figures/007_Figure_5.jpg]]
*Figure 5: Sampling ratio ablation with fixed K=2, ∆=0.5. Classification accuracy as a function of the sampling ratio r*

## 定位与知识库关联

### 1. 问题定位：M-RoPE 时序编码的非平滑瓶颈

PAS 并非提出新的位置编码方案，而是对现有 M-RoPE 的推理时缺陷进行精准修复。M-RoPE 在视频 LLM 中被广泛采用，其核心机制是将旋转位置编码的频率线集合沿时间轴展开，通过逆傅里叶变换（IFT）核 $m(\Delta) = \frac{1}{m}\sum_{i=0}^{m-1} e^{\mathrm{j}\omega_i \Delta}$ 对注意力 logit 施加时序调制。然而，$m(\Delta)$ 由有限离散频率线的余弦平均构成，在帧尺度上存在**固有波纹（非平滑）**：相邻帧的注意力被乘以差异显著的调制因子，当关键帧恰好落入调制波形的低增益波谷时，其信息被抑制甚至忽略，注意力决策被偶然的时序偏移而非内容相似性主导（Figure 1 展示了这一失败模式）。

PAS 的核心洞察来自 **定理 1** 的相位调制近似：在高维多线近似下，RoPE 旋转后的注意力 logit 可分解为未旋转的内容点积与标量 IFT 调制因子的乘积：
$$\langle \tilde{\mathbf{q}}, \tilde{\mathbf{k}} \rangle (\Delta) \approx \langle \mathbf{q}, \mathbf{k} \rangle \cdot \mathrm{Re}\{ m(\Delta) \}$$
这一分解将内容相似性与时序调制解耦，揭示了时间不稳定的根源在于调制核 $m(t)$ 的非平滑性。**定理 2** 进一步将注意力对微小时间偏移的稳定性与 $m(t)$ 的最大局部斜率 $L_m$ 绑定：
$$\big| A(\Delta t + \delta t) - A(\Delta t) \big| \leq \big| \langle \mathbf{q}, \mathbf{k} \rangle \big| L_m |\delta t|$$
更平滑的 $m(t)$ 意味着更小的 $L_m$ 和更稳定的注意力决策。

### 2. 方法谱系：训练无关推理时方法的继承与超越

PAS 属于**训练无关、推理时即插即用**的方法家族，与以下基线工作共享这一设计哲学：

- **SlowFast-LLaVA**：通过慢速（低 FPS 高空间细节）和快速（高 FPS 激进下采样）双路径稳定决策，本质是在输入层面增加时序覆盖的冗余度。
- **TS-LLaVA**：通过紧凑缩略图保留全局空间线索与轻量时序采样流混合，扩展时间覆盖，同样在输入层面进行时序信息重组。

PAS 与上述方法的根本区别在于**干预层级**：SlowFast 和 TS-LLaVA 作用于视频 token 化/采样阶段，通过改变输入帧的选择和排列来缓解时序不稳定；PAS 则直接作用于**注意力计算的内部机制**——仅修改查询流 Q 的时序相位，不改变任何 token 化、帧数量或模型参数。这一设计使 PAS 具有独特的**可堆叠性**：实验表明，将 PAS 叠加在 SlowFast-LLaVA 或 TS-LLaVA 之上可带来进一步的性能提升（Table 1：20BN-Jester 上 SlowFast+PAS 达 19.6，TS-LLaVA+PAS 达 19.3，均优于各自单独使用），证明 PAS 解决的时序非平滑问题与输入层面的时序覆盖扩展是**正交且互补**的。

在更广泛的知识库中，PAS 的平滑思想与以下方向形成对话：

- **多头注意力的隐式集成**：标准多头注意力本身已通过不同头的参数化实现某种隐式集成，但 PAS 首次显式地将**相位偏移作为可控的平滑旋钮**引入时序维度，将多头聚合重新解释为时域移动平均。
- **测试时自适应与推理时优化**：与需要梯度更新的测试时优化方法（如 TENT、T3A）不同，PAS 是纯前向的确定性操作，无任何学习或优化过程。
- **位置编码的平滑性研究**：在 NLP 领域，ALiBi、KERPLE 等工作关注位置编码的外推平滑性；PAS 则将平滑性分析引入视频时序域，且聚焦于**推理时修复**而非训练时设计。

### 3. 适用边界与前提条件

PAS 的适用性受以下前提约束：

1. **底层模型必须使用 M-RoPE 且具备独立的时序维度编码**。PAS 的相位旋转算子 $\Gamma_\delta$ 仅作用于时序半维度，依赖 M-RoPE 将频率线沿时间轴展开的结构。对于使用绝对位置编码、可学习位置编码或其他 RoPE 变体（如仅空间 RoPE）的模型，PAS 无法直接移植。

2. **Nyquist 采样条件的满足程度影响增益幅度**。定理 4 保证在 Nyquist 带限假设下，每头时序偏移仅改变 DFT 相位而不改变幅值（$|X_\delta[k]| = |X[k]|$）。当有效时序采样满足 Nyquist 条件时，PAS 的平滑操作在理论上无损；当欠采样时（如 Breakfast Actions 数据集），混叠效应限制了有效收益——Table 2 明确标注了各基准的 Nyquist 满足情况，Breakfast Actions 的改进窗口更窄且绝对增益较小，与此理论预测一致。

3. **采样率与增益的反比关系**。Figure 5 的采样率消融实验揭示了关键边界：PAS 在低采样率下增益最大，随采样率 $r$ 增大逐渐收敛至与原始 backbone 统计不可区分。这与定理 2 的预测一致——密集采样本身已提供了对 IFT 核的充分平滑探测，减少了推理时平滑的空间。这意味着 PAS 的价值主要体现在**稀疏采样场景**（如长视频理解中为控制 token 预算而降低帧率），而非已充分采样的短 clip。

4. **仅作用于时序维度，空间编码不变**。PAS 的 $\Gamma_\delta$ 仅作用于时序半维度，对于主要依赖空间线索的任务（如静态场景识别），改进可能有限。当前实验覆盖的动作识别和时序推理基准均具有显著的时序依赖性，PAS 在纯空间任务上的效果需进一步验证。

### 4. 局限性与开放问题

**已确认的局限**：

- **高采样率下增益消失**：当采样率足够高时，PAS 与原始 backbone 性能统计不可区分（Figure 5），密集采样本身已平滑了 IFT 核的有效探测。
- **Nyquist 欠采样场景收益受限**：混叠效应限制了有效收益（Breakfast Actions 的改进窗口更窄）。
- **依赖 M-RoPE 架构**：不适用于其他位置编码方案，限制了跨架构的通用性。
- **当前默认设置为手工设定**：K=2 分组、$\Delta=0.5$ bin 单位虽在实践中表现良好且具有广泛平台效应（Figure 4 显示 $\Delta$ 在 0.3-0.8 范围内增益稳定），但未探索自适应调整策略。

**开放问题**：

1. **分组数 K 的扩展性与收益递减**：当前默认 K=2，更多分组数（K=3, K=4 等）是否能带来进一步的平滑收益？收益是否随 K 增加而递减？这涉及平滑效果与计算开销的权衡。

2. **相位偏移量的自适应学习**：偏移量是否可以端到端学习，而非手工设定？学习到的偏移量分布是否与理论分析一致？是否可随视频长度或内容动态调整（如极长视频 EgoSchema 场景下的自适应策略）？

3. **聚合权重的优化**：当前聚合权重 $a_h$ 为均匀分布，非均匀加权（如根据频率线分布或注意力头的重要性进行优化）是否能进一步提升平滑效果？

4. **跨模态迁移**：PAS 的相位平滑机制是否适用于其他基于 RoPE 的多模态场景？例如音频时间轴、3D 视频的深度维度、或医学影像的切片序列——任何使用 M-RoPE 进行一维时序/序列编码的场景理论上均可受益。

5. **与其他推理时方法的组合**：PAS 与多 pass 平均、Temporal Coherent Test-Time Optimization 等方法的组合效果如何？PAS 的可堆叠性已在 SlowFast/TS-LLaVA 上验证，但更广泛的推理时方法组合空间尚未探索。

6. **视频分词策略的影响**：不同的视频分词和帧合并策略（如均匀采样 vs. 关键帧提取）如何影响 PAS 的最优偏移量选择？这涉及 token 化阶段的时序粒度与注意力阶段平滑操作的匹配问题。

## 原文 PDF

![[paperPDFs/CVPR_2026/PAS_A_Training_Free_Stabilizer_for_Temporal_Encoding_in_Video_LLMs.pdf]]

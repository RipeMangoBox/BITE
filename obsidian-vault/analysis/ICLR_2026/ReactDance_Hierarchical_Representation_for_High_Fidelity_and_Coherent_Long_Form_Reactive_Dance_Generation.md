---
title: "ReactDance: Hierarchical Representation for High-Fidelity and Coherent Long-Form Reactive Dance Generation"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/ReactDance_Hierarchical_Representation_for_High_Fidelity_and_Coherent_Long_Form_Reactive_Dance_Generation.pdf
project_link: https://ripemangobox.github.io/ReactDance
code_link: null
openreview_forum_id: FvMyAMbbX0
aliases:
- ReactDance
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/vision_models_multimodal
core_operator: "利用分层有限标量量化（HFSQ）解耦粗/细运动语义，并引入块级局部上下文（BLC）并行采样与层解耦无分类器引导（LDCFG）的多尺度调控机制，从而同时提升空间精度与长期连贯性。"
primary_logic: "借鉴舞蹈编舞中层次化运动组合与模块化连贯性原理，通过HFSQ构建从粗粒度姿态到细粒度动态的分层表示，并利用密集滑动窗口训练赋予解码器相位无关的过渡能力，最终以并行块采样实现高效且连贯的长序列生成。"
claims:
- "ReactDance在DD100测试集上取得5.57的FID_k及1.75秒的平均推理时间，显著超越所有对比方法，验证了高保真与高效生成。"
- "移除HFSQ或渐进掩码（PM）导致FID_g由7.63上升至10.46，并产生空间交互错误，证明分层表示与掩码正则至关重要。"
- "BLC的密集滑动窗口（DSW）与相位对齐位置编码是长期连贯的关键，将训练步长s由4增大至64会使交互FID_cd由14.17急升至39.50。"
- "层解耦无分类器引导（LDCFG）通过独立控制粗/细尺度权重，可在S=[1.2,1.2]处实现保真度与交互质量的最优平衡。"
---

# ReactDance: Hierarchical Representation for High-Fidelity and Coherent Long-Form Reactive Dance Generation

> [!tip] 核心洞察
> 借鉴舞蹈编舞中层次化运动组合与模块化连贯性原理，通过HFSQ构建从粗粒度姿态到细粒度动态的分层表示，并利用密集滑动窗口训练赋予解码器相位无关的过渡能力，最终以并行块采样实现高效且连贯的长序列生成。

| 字段 | 内容 |
|------|------|
| 中文题名 | ReactDance：面向高保真与连贯长序列交互舞蹈生成的分层表示 |
| 英文题名 | ReactDance: Hierarchical Representation for High-Fidelity and Coherent Long-Form Reactive Dance Generation |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=FvMyAMbbX0) · [Project](https://ripemangobox.github.io/ReactDance) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/vision_models_multimodal |
| Method | ReactDance |
| Dataset | DD100 |

> [!tip] 效果简介
> - DD100 (测试集，平均长度2066帧) 上，FID_k ↓ 5.57 vs Duolando 27.68 (-22.11)。
> - DD100 上，MPJPE ↓ 132.99 vs Duolando 174.54 (-41.55)；FID_cd ↓ 14.17 vs Duolando 17.49 (-3.32)；AITS (s) ↓ 1.75 vs EDGE 2.91 (-1.16)。

## 概要

反应舞蹈生成（Reactive Dance Generation, RDG）要求模型根据领舞者运动与音乐实时合成自然、连贯且富有表现力的反应动作，其核心挑战在于**细粒度空间交互的准确建模**与**长序列时间一致性的维持**。现有方法或依赖全局高层约束而忽视局部关键动作，或因训练与推断的长度不匹配导致误差累积与同步漂移，难以同时满足高保真与长序列连贯的需求。

ReactDance 提出了一种**分层有限标量量化（Hierarchical Finite Scalar Quantization, HFSQ）**的运动表示，将反应者动作从粗粒度姿态到细粒度动态进行解耦建模，并配合**块级局部上下文（Blockwise Local Context, BLC）并行采样**与**层解耦无分类器引导（Layer-Decoupled Classifier-Free Guidance, LDCFG）**，在保持高推理效率的同时实现长序列的连贯生成。其核心洞察源于舞蹈编舞中层次化运动组合与模块化连贯性原理：通过 HFSQ 构建多尺度潜空间，利用密集滑动窗口训练赋予解码器相位无关的过渡能力，最终以并行块采样替代传统自回归方式。

在 DD100 测试集（平均长度 2066 帧）上，ReactDance 取得 **FID_k 5.57**，较此前最佳的专用反应舞蹈模型 Duolando（27.68）降低 22.11；交互质量指标 FID_cd 降至 14.17，平均推理时间仅 1.75 秒，**在保真度、交互质量与效率三个维度均显著超越所有对比方法**（Table 1）。消融实验进一步证实：移除 HFSQ 或渐进掩码策略会导致生成 FID 恶化并引入空间交互错误（Table 2, Figure 6, Figure 7）；扩大训练步长或舍弃 BLC 的相位对齐机制则使交互指标急剧下降（Table 3, Table 6），验证了分层表示与并行采样策略对长期连贯性的关键作用。



### 问题定义：反应舞蹈生成

反应舞蹈生成（Reactive Dance Generation, RDG）要求根据领舞者的运动序列与音乐输入，生成与之空间协调、时间同步的反应者舞蹈。与单人舞蹈生成或文本驱动的动作合成不同，RDG的核心挑战在于**双向人际动态的精准建模**——反应者不仅需要保持自身动作的物理合理性与音乐节奏对齐，更必须在每一帧与领舞者维持恰当的空间关系与交互语义。

### 现有方法的瓶颈

当前RDG方法主要沿两条路径展开：一是将成熟的单人生成模型适配至双人场景，如**GestureLSM**（Liu et al., 2025）、**EDGE**（Tseng et al., 2023）、**TCDiff**（Dai et al., 2025）及**InterGen**（Liang et al., 2024）；二是专用模型如**Duolando**（Siyao et al., 2024）。然而，这些方法普遍面临两大未解决瓶颈：

**瓶颈一：细粒度空间交互建模不足。** 现有方案多依赖全局高层约束（如相对距离、朝向差异）来调控双人关系，却忽视了局部关键动作的精细对齐——例如手部接触、头部呼应等细节直接决定了交互的自然度。当领舞者做出微妙手势时，反应者常出现相对距离错误或手部交互失配（见Figure 6红色标注区域），暴露出全局约束对局部动态的感知盲区。

**瓶颈二：长期时间一致性难以维持。** 训练阶段模型仅在固定长度的短窗口上优化，而推理时需生成远超训练窗口的长序列（DD100测试集平均长度达2066帧）。这种训练-推断的长度不匹配导致误差逐步累积，最终引发同步漂移与动作质量退化。Figure 5的定性对比清晰展示了这一点：InterGen在超出训练视野后动作坍缩为不真实抖动，Duolando则产生不自然的头部旋转。

### 核心动机：层次化与模块化的编舞原理

本工作的动机源于对舞蹈编舞本质的观察：专业编舞者并非逐帧设计动作，而是遵循**从粗到细的层次化组合**与**模块化连贯性**原则——先确定身体姿态与空间占位（粗粒度结构），再填充关节动态与节奏细节（细粒度表现），最终将动作片段无缝拼接为长序列。然而，现有生成范式将上述多层语义压缩至扁平潜空间，或用自回归方式逐段生成，既丧失了层次化表达带来的解耦优势，又因串行推断牺牲了效率与长程连贯性。

ReactDance正是为了填补这一鸿沟而提出：通过构建**分层表示**来显式解耦粗/细运动语义，并设计**并行采样机制**来突破序列长度的限制，从而在单一框架内同时实现高保真空间交互与连贯长序列生成。



## 核心方法与创新机理

ReactDance 针对反应舞蹈生成（Reactive Dance Generation, RDG）中长期存在的**细粒度空间交互建模不足**与**长序列时间一致性崩溃**两大瓶颈，提出了一套以分层表示为核心的生成框架。其关键创新可归结为三个相互耦合的 changed slots，分别重塑了运动表示、采样策略与条件引导机制。

---

### 1. 运动表示：从扁平潜变量到分层有限标量量化（HFSQ）

现有方法普遍采用 VQ-VAE 或扁平连续潜变量对运动进行编码，难以同时捕获粗粒度姿态结构与高频动态细节。ReactDance 提出**分层有限标量量化**（Hierarchical Finite Scalar Quantization, HFSQ），将反应者运动（分解为上肢、下肢、相对根位移三个独立组件）编码为一组具有层级语义的连续表示：

$$
\mathcal{V} = \{\hat{v}_{g,r}\}_{g=1,r=1}^{G,R}
$$

其中 $G$ 为分组数，$R$ 为每组内的残差阶段数（最终设置 $R=2$）。编码器输出的特征被划分为 $G$ 组，每组依次经过 $R$ 级级联残差 FSQ：每一级对当前残差进行有限标量量化与反量化，再将重建残差从输入中减去，传递至下一级。这一设计借鉴了神经音频编解码器的残差量化思想，但通过**分组并行**与**有限标量量化**消除了传统 VQ 中常见的码本坍缩问题，同时赋予潜空间从粗到细的多尺度运动表现力。

**消融证据**：当用 RVQ-VAE 替代 HFSQ 时，生成 FID（FID_g）从 7.63 恶化至 10.46，并出现错误的手部交互与相对距离偏差（Table 2, Figure 6），证实分层表示对精细空间交互建模的因果必要性。

---

### 2. 长序列采样：从自回归生成到块级局部上下文（BLC）并行采样

自回归逐帧或逐段生成是现有方法的默认范式，但其训练-推断长度不匹配导致误差累积与同步漂移，严重制约长序列的连贯性。ReactDance 提出**块级局部上下文**（Blockwise Local Context, BLC）并行采样策略，将完整时间线划分为若干块，在每块内并行去噪，同时通过两个关键设计保证块间连贯：

- **周期因果掩码**（Periodic Causal Mask, PCAM）：强制每个块内的帧仅关注自身及历史上下文，模拟训练时的滑动窗口感受野。
- **相位对齐位置编码**（Phase-aligned Positional Encoding, PPE）：

$$
\mathcal{P}_i = \sin\left(\frac{\pi (i \bmod T)}{T}\right) \oplus \cos\left(\frac{\pi (i \bmod T)}{T}\right)
$$

将每个块的时间相位重置为训练窗口内的相位，使解码器以相位无关的方式理解相邻潜变量之间的过渡关系。

这一采样策略的有效性依赖于**密集滑动窗口**（Dense Sliding Window, DSW）训练：以步长 $s=4$ 的密集窗口训练解码器，使其学会在任意窗口边界处产生连续运动。消融显示，将 $s$ 从 4 增大至 64 时，交互 FID（FID_cd）从 14.17 急剧恶化至 39.50（Table 3, Table 6）；若用潜空间拼接替代 PPE 和 PCAM，AITS 从 1.75s 增至 2.03s，FID_cd 恶化至 42.10（Table 3），证明 DSW 训练与相位对齐机制是长序列连贯性的因果杠杆。

---

### 3. 条件引导：从单一全局尺度到层解耦无分类器引导（LDCFG）

标准无分类器引导对所有特征维度施加统一的引导强度，无法区分粗粒度姿态与细粒度动态对条件信号的不同依赖程度。ReactDance 提出**层解耦无分类器引导**（Layer-Decoupled Classifier-Free Guidance, LDCFG），为 HFSQ 的每个残差层级 $r$ 分配独立的引导强度 $s_r$：

$$
\hat{\pmb{x}}_0^r = (1 + s_r) \mathcal{G}_{\theta}(\pmb{x}_t^r, t, \pmb{c}, \mathbf{M}_L) - s_r \mathcal{G}_{\theta}(\pmb{x}_t^r, t, \emptyset, \emptyset)
$$

通过在去噪过程中对粗、细尺度施加差异化的条件放大，LDCFG 实现了保真度与交互质量之间的精细权衡。实验表明，当 $S=[1.2, 1.2]$ 时，模型在单人运动质量与双人交互精度之间取得最优折衷（Table 4）。此外，LDCFG 可进一步扩展至身体部位级别的解耦控制，通过对下肢、上肢或全局运动施加不同引导强度，实现多样化的艺术风格操控（Figure 8）。

---

### 创新耦合与因果链路

上述三个 changed slots 并非孤立改进，而是形成了一条清晰的因果链路：**HFSQ 提供多尺度解耦的潜空间**，使扩散模型能够分层建模从姿态到动态的运动语义；**BLC 并行采样**利用 DSW 训练赋予解码器的相位无关过渡能力，在该潜空间上实现高效且连贯的长序列生成；**LDCFG** 则在这一分层潜空间上施加多尺度引导，独立调控粗、细层级的条件响应强度。三者协同，使得 ReactDance 在 DD100 测试集（平均长度 2066 帧）上以 1.75 秒的平均推理时间取得 5.57 的 FID_k，显著超越专用 RDG 模型 **Duolando**（Siyao et al., 2024）的 27.68（Table 1），同时将 MPJPE 从 174.54 降至 132.99，验证了分层表示对高保真与高效率生成的决定性作用。



ReactDance 是一个两阶段扩散框架，以领舞者运动 $\mathbf{M}_L$ 与音乐特征 $\mathbf{c}$ 为条件，生成高保真、长序列的反应者舞蹈（**Figure 4**）。其核心设计遵循“层次化表示—扩散生成—并行采样”的流水线，通过解耦粗/细运动语义，同时提升空间交互精度与长期时间连贯性。

![[assets/figures/papers/reactdance_tag_link_fix_20260602/figures/004_Figure_4.jpg]]
*Figure 4: ReactDance Pipeline Overview. Our ReactDance generates long, high-fidelity reactive dance sequences conditioned on leader motion and music. The core is a diffusion model that learns to denoise hierarchical HFSQ latents. Leader motion is injected via cross-attention, while music features are fused using a FiLM layer. For coherent generation of long sequences, our Blockwise Local Context (BLC) sampling strategy partitions the timeline into parallel blocks with aligned temporal contexts. Within each denoising step, Layer-Decoupled Classifier-Free Guidance (LDCFG) provides fine-grained control by applying independent guidance weights to each HFSQ scale. Finally, the denoised latents are decoded...*

### 两阶段生成流程

**第一阶段：HFSQ 自动编码器。** 反应者运动被分解为三个独立组件——上肢运动 $\mathbf{M}_{Rup}$、下肢运动 $\mathbf{M}_{Rdown}$ 及相对根位移 $\mathbf{M}_{tr}$，经 1D 卷积编码器压缩为特征序列后，送入分层有限标量量化器（Hierarchical Finite Scalar Quantization, HFSQ）。HFSQ 将特征按 $G$ 组进行 $R$ 级残差级联量化，输出层次化连续表示 $\mathcal{V} = \{\hat{v}_{g,r}\}_{g=1,r=1}^{G,R}$（**Figure 2**），其中粗粒度层级捕获身体姿态，细粒度层级编码高频动态。解码器从量化特征重建运动组件，完成“编码—量化—重建”闭环。

**第二阶段：分层潜扩散模型。** 以 HFSQ 潜变量 $\mathcal{V}$ 为生成目标，基于 Transformer 的扩散模型在潜空间上逐步去噪。领舞者运动通过交叉注意力注入，音乐特征则经 FiLM 层融合。去噪过程受层解耦无分类器引导（Layer-Decoupled Classifier-Free Guidance, LDCFG）调控——各残差层拥有独立的引导强度 $s_r$，实现粗/细尺度的精细控制：

$$\hat{\pmb{x}}_0^r = (1 + s_r) \mathcal{G}_{\theta}(\pmb{x}_t^r, t, \pmb{c}, \mathbf{M}_L) - s_r \mathcal{G}_{\theta}(\pmb{x}_t^r, t, \emptyset, \emptyset)$$

**推理采样：BLC 并行采样。** 为生成超长序列（>2000 帧），块级局部上下文（Blockwise Local Context, BLC）策略将时间轴划分为多个块，应用周期因果掩码（PCAM）与相位对齐位置编码（PPE），使各块在保留局部时间上下文的前提下并行去噪。相位对齐位置编码将每块的时间相位重置为训练窗口内的相位：

$$\mathcal{P}_i = \sin\left(\frac{\pi (i \bmod T)}{T}\right) \oplus \cos\left(\frac{\pi (i \bmod T)}{T}\right)$$

这种设计依赖于密集滑动窗口（Dense Sliding Window, DSW）训练——解码器在训练阶段被赋予相位无关的过渡能力，确保块间边界运动连续，避免自回归方法的误差累积与同步漂移。

### 关键模块关系

| 模块 | 功能 | 证据锚点 |
|------|------|----------|
| 运动编码器（1D 卷积） | 将反应者运动序列压缩为特征序列 | Section 3.2 |
| HFSQ 量化器 | 分组级联残差 FSQ，输出分层潜变量 $\mathcal{V}$ | Section 3.2, Figure 2 |
| 运动解码器 | 从量化特征重建运动组件 | Section 3.2 |
| 分层扩散 Transformer | 在 HFSQ 潜空间上以领舞者与音乐为条件逐步去噪 | Section 3.3, Figure 4 |
| BLC 并行采样引擎 | 块划分 + PCAM + PPE 实现并行生成，DSW 训练保证块间连贯 | Section 3.4 |
| LDCFG 多尺度控制 | 各残差层独立引导强度，平衡保真度与交互质量 | Section 3.5 |

### 输入输出流

**输入：** 领舞者运动序列 $\mathbf{M}_L$（SMPL 姿态参数）与音乐特征 $\mathbf{c}$（预提取的音频表示）。

**输出：** 反应者运动组件 $\mathbf{M}_R = \{\mathbf{M}_{Rup}, \mathbf{M}_{Rdown}, \mathbf{M}_{tr}\}$，经 SMPL 模型组合为完整反应舞蹈序列，长度可超过 2000 帧，推理时间约 1.75 秒（**Table 1**）。

**数据流路径：** 领舞者运动经交叉注意力注入扩散 Transformer → 音乐特征经 FiLM 调制扩散过程 → 随机噪声在 HFSQ 潜空间逐步去噪为 $\mathcal{V}$ → HFSQ 解码器将 $\mathcal{V}$ 重建为反应者运动组件 → 组件组合为最终舞蹈序列。



ReactDance 采用两阶段框架：首先训练一个带分层有限标量量化（HFSQ）瓶颈的自编码器，将反应者运动压缩为分层潜表示；随后在该潜空间上训练一个条件扩散模型，以领舞者运动和音乐为条件进行去噪生成。以下按流水线顺序阐述关键模块及其核心公式。

---

### 运动编码器与解码器（1D 卷积）

反应者运动被分解为三个独立组件：上肢运动 $\mathbf{M}_{Rup}$、下肢运动 $\mathbf{M}_{Rdown}$ 以及相对根节点距离 $\mathbf{M}_{tr}$（Section 3.1）。运动编码器采用 1D 卷积将这些组件压缩为特征序列，解码器则从量化后的特征重建运动组件。该分解策略使模型能分别关注不同身体部位的运动学特性。

---

### HFSQ 量化器：分层有限标量量化

HFSQ 是本文的核心表示创新，其设计借鉴神经音频编解码器中的残差量化思想，但消除了码本坍缩问题，同时增强了多尺度运动表现力（Figure 2）。具体而言，编码器输出的特征被分为 $G$ 组，每组经历 $R$ 个残差阶段（本文取 $G=2, R=2$）：

![[assets/figures/papers/reactdance_tag_link_fix_20260602/figures/002_Figure_2.jpg]]
*Figure 2: Motion HFSQ overview. The proposed motion HFSQ learns to progressively encode motion sequence into a hierarchical representation $\mathcal { V } = \left\{ \hat { v } _ { g , r } \right\} _ { g = 1 , r = 1 } ^ { G , R }$ and reconstructs motions via a grouped residual architecture. Building on FSQ, HFSQ eliminates codebook collapse while enhancing multi-scale motion expressiveness through grouped residual quantization, which integrates coarse-to-fine motion semantics

**级联残差量化过程**（Section 3.2）：

$$z_{g,r} = \mathrm{FSQ}_r(e_{g,r}); \quad \hat{v}_{g,r} = \mathrm{Dequantize}(z_{g,r}); \quad e_{g,r+1} = e_{g,r} - s_r \cdot \hat{v}_{g,r}.$$

其中 $e_{g,1}$ 为第 $g$ 组的初始编码特征，$\mathrm{FSQ}_r$ 为第 $r$ 阶段的有限标量量化器，$s_r$ 为可学习的缩放因子。每一阶段量化并重建当前残差后，将其从特征中减去，剩余部分进入下一阶段。这种级联设计使得浅层（$r=1$）捕获粗粒度姿态信息，深层（$r=R$）编码高频动态细节。

**分层连续表示**（Equation (2)）：

$$\mathcal{V} = \{\hat{v}_{g,r}\}_{g=1,r=1}^{G,R}.$$

$\mathcal{V}$ 是所有组、所有残差阶段重建特征的集合，构成扩散模型的目标潜空间。与扁平 VQ-VAE 潜变量不同，$\mathcal{V}$ 天然具备从粗到细的语义层次。

**HFSQ 总损失**（Equation (3)）：

$$\mathcal{L}_{\mathrm{HFSQ}} = \lambda_{kin} \mathcal{L}_{\mathrm{kinematic}} + \lambda_{lat} \mathcal{L}_{latent}.$$

其中 $\mathcal{L}_{\mathrm{kinematic}}$ 为运动学重建损失（包含位置、速度、加速度等约束），$\mathcal{L}_{latent}$ 为潜变量对齐损失。

**潜变量损失**（Equation (5)）：

$$\mathcal{L}_{latent} = \| \pmb{v} - \mathrm{sg}(\hat{\pmb{v}}) \|_2^2 + \beta \| \mathrm{sg}(\pmb{v}) - \hat{\pmb{v}} \|_2^2.$$

其中 $\pmb{v}$ 为编码器输出，$\hat{\pmb{v}}$ 为量化后特征，$\mathrm{sg}(\cdot)$ 为 stop-gradient 操作，$\beta$ 为承诺损失权重。该对称损失确保编码器输出向量化特征靠拢，同时量化特征也向编码器输出对齐。

---

### 渐进掩码（Progressive Masking）

为增强解码器对潜变量扰动的鲁棒性，训练时施加两种掩码策略（Figure 3）：

![[assets/figures/papers/reactdance_tag_link_fix_20260602/figures/003_Figure_3.jpg]]
*Figure 3: Progressive masking overview*

- **残差掩码**：随机遮蔽高层 FSQ 层的输出，同时对基础层施加缩放高斯噪声，迫使各层学习独立且互补的运动信息。
- **代码掩码**：在单个 FSQ 编码内部随机遮蔽部分维度，提升解码器对量化误差的容错能力。

消融实验证实，移除渐进掩码导致生成 FID_g 从 7.63 升至 10.46，并产生交互穿透伪影（Table 2, Figure 7）。

---

### 基于 Transformer 的分层扩散模型

扩散模型在 HFSQ 潜空间 $\mathcal{V}$ 上运行，以领舞者运动 $\mathbf{M}_L$ 和音乐特征 $\mathbf{c}$ 为条件。领舞者运动通过交叉注意力注入，音乐特征通过 FiLM 层融合（Figure 4）。

**分层扩散简化损失**（Equation (6)）：

$$\mathcal{L}_{\mathrm{simple}} = \sum_{r=1}^{R} \lambda^{r} \cdot \mathbb{E}_{\mathbf{x}_0,t,\epsilon} \left[ \| \mathcal{V}^{r} - \mathcal{G}_{\theta}(\mathbf{x}_t, t, c, \mathbf{M}_L)^r \|_2^2 \right].$$

其中 $\mathcal{V}^{r}$ 为第 $r$ 层 HFSQ 潜变量的真实值，$\mathcal{G}_{\theta}$ 为去噪网络，$\lambda^r$ 为各层权重。该损失对每个残差层级独立计算 L2 期望，使模型能分层学习不同粒度的运动语义。

**扩散总损失**（Equation (7)）：

$$\mathcal{L}_{\mathrm{diffusion}} = \mathcal{L}_{\mathrm{simple}} + \lambda_{\mathrm{kin}} \mathcal{L}_{\mathrm{kinematic}} + \lambda_{\mathrm{fc}} \mathcal{L}_{\mathrm{fc}} + \lambda_{\mathrm{ro}} \mathcal{L}_{\mathrm{ro}}.$$

除简化损失外，额外引入运动学损失 $\mathcal{L}_{\mathrm{kinematic}}$（位置/速度约束）、脚步接触损失 $\mathcal{L}_{\mathrm{fc}}$ 和相对方向损失 $\mathcal{L}_{\mathrm{ro}}$，以增强生成运动的物理合理性。

---

### BLC 并行采样引擎

块级局部上下文（BLC）采样是实现长序列高效生成的核心机制（Section 3.4）。其关键组件包括：

**相位对齐位置编码**（Equation (8)）：

$$\mathcal{P}_i = \sin\left(\frac{\pi (i \bmod T)}{T}\right) \oplus \cos\left(\frac{\pi (i \bmod T)}{T}\right).$$

其中 $T$ 为训练窗口长度，$i$ 为帧索引。该编码将每个生成块的时间相位重置为训练窗口内的相位，使解码器能以相位无关的方式处理块边界过渡。

**周期因果掩码（PCAM）**：在块内施加因果注意力，同时允许跨块并行计算，确保时序一致性而不牺牲并行效率。

**密集滑动窗口（DSW）训练**：训练时以步长 $s=4$ 的密集滑动窗口采样片段，赋予解码器理解任意窗口边界处运动连续性的能力。消融表明，将 $s$ 从 4 增至 64 会使交互 FID_cd 从 14.17 急剧恶化至 39.50（Table 3, Table 6），验证了密集训练对长期连贯性的关键作用。

---

### LDCFG 多尺度控制

层解耦无分类器引导（LDCFG）为 HFSQ 各残差层分配独立的引导强度 $s_r$（Section 3.5）：

**LDCFG 去噪预测**（Equation (9)）：

$$\hat{\pmb{x}}_0^r = (1 + s_r) \mathcal{G}_{\theta}(\pmb{x}_t^r, t, \pmb{c}, \mathbf{M}_L) - s_r \mathcal{G}_{\theta}(\pmb{x}_t^r, t, \emptyset, \emptyset).$$

其中 $s_r$ 为第 $r$ 层的引导强度，$\emptyset$ 表示空条件。与标准 CFG 使用单一全局尺度不同，LDCFG 允许对粗粒度层（控制整体姿态）和细粒度层（控制局部动态）施加不同的引导权重。实验表明，设置 $S=[1.2, 1.2]$ 可获得保真度与交互质量的最优平衡（Table 4），且该机制可进一步扩展为对身体部位（下肢、上肢、全局）施加差异化引导，实现细粒度艺术控制（Figure 8）。

### 补充图表

![[assets/figures/papers/reactdance_tag_link_fix_20260602/figures/009_Figure_6.jpg]]
*Figure 6: Qualitative comparison for the HFSQ ablation. While our full model maintains correct spatial relationships, the model trained without HFSQ (using an RVQ-VAE) fails to capture precise inter-personal dynamics, resulting in incorrect relative distancing and mismatched hand interactions (highlighted in red circles)*



## 实验与关键发现

### 主结果：长序列反应舞蹈的高保真与高效生成

ReactDance在DD100测试集（平均序列长度2066帧）上进行了全面评估，涵盖单人运动质量、交互质量、音乐对齐及推理效率。如**Table 1**所示，ReactDance在所有核心指标上均显著超越现有方法，包括专门针对反应舞蹈生成（RDG）设计的**Duolando**（Siyao et al., 2024）以及经适配的单人/多人模型。

![[assets/figures/papers/reactdance_tag_link_fix_20260602/figures/005_Table_1.jpg]]
*Table 1: Comparison with state-of-the-art methods on the test dataset of DD100 dataset. Symbols ↑, ↓, and → indicate the higher, lower and closer to Ground Truth are better. Bold and underline indicate the best and second best results. The dotted line separates methods for single-person motion generation (above) from those for duet and multi-person generation (below)*

- **运动保真度**：ReactDance取得**FID_k = 5.57**，较最优基线Duolando（27.68）降低**22.11**，降幅达79.9%。在全局运动质量指标**FID_g**上，ReactDance亦达到7.63，远优于其他方法。这表明分层表示有效捕获了从粗粒度姿态到细粒度动态的多尺度运动分布。
- **交互精度**：在反应者与领舞者的空间关系上，ReactDance的**MPJPE**降至**132.99 mm**（Duolando为174.54 mm），**FID_cd**（交互距离FID）为**14.17**（Duolando为17.49）。这验证了HFSQ对细粒度人际空间动态的建模能力。
- **推理效率**：得益于BLC并行采样策略，ReactDance的**平均推理时间（AITS）仅为1.75秒**，显著快于EDGE（2.91秒）和Duolando（2.89秒），同时生成质量远超二者。这打破了自回归方法中“长序列生成速度慢、质量衰减”的固有瓶颈。

**Figure 5**的定性对比进一步印证了数值优势：在相同领舞者输入下，Duolando产生不自然的头部旋转，GestureLSM出现不协调交互，InterGen在超出训练时长后运动崩溃为不真实抖动；而ReactDance生成的反应流畅、连贯且与领舞者保持正确的空间关系。

**用户研究**（**Figure 9**）显示，ReactDance在运动质量、交互合理性和整体偏好等所有主观评价标准上一致优于各基线，确证了其生成结果在人类感知层面的优越性。

### 消融研究：分层表示与训练策略的关键作用

#### HFSQ与渐进掩码（PM）
**Table 2**的消融揭示了HFSQ tokenizer和渐进掩码正则化的决定性贡献：
- 用**RVQ-VAE替代HFSQ**导致**FID_g从7.63恶化至10.46**，且**Figure 6**的定性结果显示，模型丢失了精细的人际动态，产生错误的相对距离与手部交互失配。
- **移除渐进掩码（PM）**同样使FID_g升至10.46，**Figure 7**显示反应者朝向错误并出现穿透伪影。这证明残差掩码与代码掩码对增强潜空间鲁棒性和层间独立性的必要性。

#### 密集滑动窗口（DSW）与BLC采样
**Table 3**和**Table 6**系统分析了长期连贯性的关键设计：
- 将DSW训练步长**s从4增大至64**，交互质量**FID_cd从14.17急剧升至39.50**，边界Jitter显著增加。**s=4**在性能与效率间取得最优折衷。
- 若用**潜空间拼接替代BLC的相位对齐位置编码（PPE）和周期因果掩码（PCAM）**，AITS由1.75s增至2.03s，FID_cd恶化至42.10。这证实了PPE将各块时间相位重置为训练窗口内相位的机制，以及PCAM强制块间因果依赖的设计，是并行采样下维持连贯性的核心。

#### 层解耦无分类器引导（LDCFG）
**Table 4**展示了LDCFG对粗/细尺度独立控制的效果。当粗层与细层引导强度均设为**S=[1.2, 1.2]**时，单人保真度与交互质量达到最优平衡。**Figure 8**进一步展示了LDCFG对身体部位（下肢、上肢、全身）施加不同引导强度所产生的多样化风格，验证了其精细艺术控制能力。

#### 条件输入消融
**Table 8**表明：领舞者运动对结构性交互至关重要，移除后交互指标显著恶化；音乐则对精细交互真实感起关键作用，缺少音乐条件会使FID_cd上升，说明音乐提供了节奏与风格线索以塑造细腻的反应动态。

### 可扩展性与手部运动分析

**Table 5**对HFSQ残差阶段数R的分析显示，虽然更高R（如R=3）略微改善重建质量，但**R=2**在生成FID和训练成本间取得最佳平衡，验证了当前设计的合理性。

**Table 7**的手部运动分析表明，ReactDance通过HFSQ有效滤除了DD100数据集中固有的高频噪声，在手部Jitter和FID_g上显著优于Duolando。然而，由于数据噪声限制，当前模型未对手指进行精细建模，这构成了已知局限。

### 失败模式与局限性

尽管ReactDance在整体性能上表现优异，分析揭示了以下边界情况：
1. **精细手指交互缺失**：DD100数据集手部运动存在大量高频噪声与抖动，模型当前未对手指单独建模，限制了复杂手势交互（如握手、指引）的表达。
2. **层级语义可解释性不足**：HFSQ的各残差层缺乏显式语义标签，难以将特定层直接对应到“姿态”“动力”等编舞概念，降低了可控性的直观程度。
3. **极端长度与节奏变化**：固定4倍下采样率对节奏变化剧烈的舞蹈风格可能非最优；在远超训练窗口长度的极端序列上，块间连贯性仍需进一步验证。

### 补充图表

![[assets/figures/papers/reactdance_tag_link_fix_20260602/figures/007_Table_2.jpg]]
*Table 2: Ablation study of HFSQ tokenizer and the Progressive Masking (PM)*

![[assets/figures/papers/reactdance_tag_link_fix_20260602/figures/011_Table_4.jpg]]
*Table 4: Solo and Duet metrics with diverse Layer-Decoupled Classifier-Free Guidance (LDCFG) weights. Best and second-best results are in bold and underline, respectively*

![[assets/figures/papers/reactdance_tag_link_fix_20260602/figures/014_Table_5.jpg]]
*Table 5: Scalability Analysis of Residual Stages R. While higher R marginally improves reconstruction, R = 2 achieves the best generation quality (FID) and the optimal trade-off between performance and cost*

![[assets/figures/papers/reactdance_tag_link_fix_20260602/figures/015_Table_6.jpg]]
*Table 6: Full Ablation of Dense Sliding Window Stride (s). Jitter measures boundary discontinuity*

![[assets/figures/papers/reactdance_tag_link_fix_20260602/figures/016_Table_7.jpg]]
*Table 7: Hand Motion Analysis. ReactDance effectively filters out high-frequency artifacts inherent in the dataset, significantly outperforming Duolando in motion stability (lower Jitter)*

![[assets/figures/papers/reactdance_tag_link_fix_20260602/figures/017_Table_8.jpg]]
*Table 8: Ablation of Conditioning Inputs. Results indicate that the leader’s motion is crucial for structural interaction, while music is essential for fine-grained interactive realism*

![[assets/figures/papers/reactdance_tag_link_fix_20260602/figures/006_Figure_5.jpg]]
*Figure 5: Qualitative comparison of reactive dance generation. Given the same leader motion, Duolando produces unnatural head rotations and GestureLSM shows uncoordinated interactions. InterGen’s motion collapses into unrealistic jitter when generalizing beyond its training horizon. In contrast, our model generates a fluid and coherent reactive motion*



## 定位与知识库关联

### 1. 问题定位与基线方法关系

ReactDance 瞄准**反应舞蹈生成（Reactive Dance Generation, RDG）**这一尚未被充分解决的子领域。该任务要求根据领舞者的运动序列和背景音乐，生成另一舞者（反应者）在时空上协调、物理上合理的长期舞蹈序列。现有方法在该任务上存在两个核心瓶颈：**细粒度空间交互建模不足**（依赖全局高层约束而忽视局部关键动作）和**长期时间一致性难以维持**（训练与推断长度不匹配导致误差累积与同步漂移）。

论文将 RDG 的方法谱系划分为两个层级，并在 DD100 数据集上统一重新训练以进行公平比较：

**上层——单人/通用运动生成模型（经适配用于 RDG）：**
- **GestureLSM**（Liu et al., 2025）：单人生成模型，适配后用于反应舞蹈，但在交互协调性上表现不足。
- **EDGE**（Tseng et al., 2023）：音乐驱动舞蹈模型，适配后缺乏对领舞者运动的显式交互建模。
- **TCDiff**（Dai et al., 2025）：多人/群舞模型，适配后仍难以捕捉双人间的细粒度空间关系。
- **InterGen**（Liang et al., 2024）：文本到交互模型，在超出其训练时长泛化时出现运动坍缩和不真实抖动。

**下层——专用交互/反应舞蹈生成模型：**
- **Duolando**（Siyao et al., 2024）：当前唯一的专用反应舞蹈生成基线，但在长期生成中仍存在不自然的头部旋转和交互伪影。

从方法设计哲学上看，上述基线普遍采用**扁平连续潜变量或标准 VQ-VAE 表示**，并依赖**自回归逐帧/逐段生成**策略。ReactDance 的核心区分点在于将舞蹈编舞的**层次化运动组合与模块化连贯性**原理引入生成框架，通过三个关键设计改变了因果调控旋钮：

| 设计槽位 | 基线主流方案 | ReactDance 方案 | 证据锚点 |
|----------|------------|----------------|---------|
| 运动表示 | VQ-VAE 或扁平连续潜变量 | 分层有限标量量化（HFSQ），G 组 R 残差级联（R=2） | Section 3.2, Figure 2 |
| 长序列采样 | 自回归逐帧/逐段生成 | 块级局部上下文（BLC）并行采样，配合周期因果掩码与相位对齐位置编码 | Section 3.4, Figure 4 |
| 条件引导 | 标准无分类器引导（单一全局尺度） | 层解耦无分类器引导（LDCFG），各残差层独立引导强度 s_r | Section 3.5, Table 4 |

### 2. 核心方法贡献的因果机制

**HFSQ 的分层解耦机制：** HFSQ 将运动特征分组后进行级联残差有限标量量化，构建从粗粒度姿态到细粒度动态的层次表示 $\mathcal{V} = \{\hat{v}_{g,r}\}_{g=1,r=1}^{G,R}$。其关键因果效应在于：粗层（低 r）捕获身体姿态和全局结构，细层（高 r）编码高频动态和局部交互细节。消融实验证实，用 RVQ-VAE 替代 HFSQ 导致生成 FID_g 从 7.63 升至 10.46，并引入错误的相对距离和不匹配的手部交互（Table 2, Figure 6）。

**BLC 的长期连贯性保障：** BLC 将长序列划分为块进行并行采样，其有效性建立在两个子机制之上——密集滑动窗口（DSW）训练赋予解码器相位无关的过渡能力，相位对齐位置编码（PPE）确保各块的时间相位与训练窗口对齐。消融显示，将 DSW 训练步长 s 从 4 增大至 64 会使交互质量指标 FID_cd 从 14.17 急剧恶化至 39.50（Table 3, Table 6）；若用潜空间拼接替代 PPE 和周期因果掩码（PCAM），推理时间从 1.75s 增至 2.03s，FID_cd 恶化至 42.10（Table 3）。

**渐进掩码（PM）的正则化作用：** PM 通过残差掩码（随机遮挡高层 FSQ 层）和代码掩码（随机遮蔽 FSQ 码内维度）增强潜空间的鲁棒性和层间独立性。移除 PM 后 FID_g 从 7.63 升至 10.46，并产生交互穿透伪影（Table 2, Figure 7）。

**LDCFG 的多尺度精细控制：** LDCFG 对每个 HFSQ 残差层应用独立的无分类器引导强度 $s_r$，去噪预测为 $\hat{\pmb{x}}_0^r = (1 + s_r) \mathcal{G}_{\theta}(\pmb{x}_t^r, t, \pmb{c}, \mathbf{M}_L) - s_r \mathcal{G}_{\theta}(\pmb{x}_t^r, t, \emptyset, \emptyset)$。设置 $S=[1.2, 1.2]$ 可在保真度与交互质量间取得最优平衡（Table 4），且可对不同身体部位（下肢、上肢、全局）施加差异化引导以实现艺术控制（Figure 8）。

### 3. 适用边界与局限

**适用边界：**
- 任务限定于**双人反应舞蹈生成**，以领舞者运动和音乐为条件。
- 运动表示基于 SMPL 模型，分解为上肢、下肢和相对根距离三个独立组件。
- 时间下采样率为 4 倍，训练窗口为 64 帧（约 2.13 秒 @30fps）。
- 推理时通过 BLC 并行采样支持超过 2000 帧的长序列生成，平均推理时间 1.75 秒。

**已明确的局限：**
1. **手部建模缺失：** 由于 DD100 数据集手部运动存在大量高频噪声与抖动，当前模型未对手指进行精细建模，限制了复杂手势交互的表达（Table 7 显示 ReactDance 通过 HFSQ 有效滤除了高频噪声，在 Jitter 和 FID_g 上显著优于 Duolando，但手部细节本身未被建模）。
2. **层级语义不可解释：** HFSQ 的层次表示缺乏显式语义解释，各残差层对应的具体运动含义难以直接解读，降低了控制的可解释性。
3. **固定下采样率的限制：** 当前固定的 4 倍下采样率对节奏变化剧烈的舞蹈风格是否最优尚不明确。

### 4. 开放问题

1. **精细手部建模：** 如何将精细手指运动纳入分层表示，并持续利用 HFSQ 的去噪能力滤除数据集噪声？（Table 7 已初步验证 HFSQ 对手部高频伪影的滤除效果）
2. **多人与跨域泛化：** 模型在更普遍的群舞场景（多于两人）或非舞蹈类交互（如体育配合）中的泛化性能如何？当前仅在双人舞蹈场景下验证。
3. **层级语义解耦：** 能否为 HFSQ 的各个残差层赋予明确且可解释的运动语义（如“姿态”“动力”“接触”等），以提升可控性和可编辑性？
4. **自适应时间压缩：** 是否需要自适应的时间压缩策略以应对节奏变化剧烈的舞蹈风格？Table 5 显示残差阶段数 R=2 在重建质量、生成 FID 与训练成本间取得最佳平衡，但时间维度的自适应尚未探索。
5. **可扩展性自动调节：** 在更大规模、更多样化的数据集上，HFSQ 的分组数目 G 和残差阶段 R 应如何自动调节以实现最优表示？当前 G 和 R 为手工设定。



## 原文 PDF

![[paperPDFs/ICLR_2026/ReactDance_Hierarchical_Representation_for_High_Fidelity_and_Coherent_Long_Form_Reactive_Dance_Generation.pdf]]

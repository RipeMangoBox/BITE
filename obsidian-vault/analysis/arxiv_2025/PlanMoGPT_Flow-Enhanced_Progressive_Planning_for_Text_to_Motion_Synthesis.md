---
title: "PlanMoGPT: Flow-Enhanced Progressive Planning for Text to Motion Synthesis"
type: paper
paper_level: A
venue: arXiv
year: 2025
pdf_ref: paperPDFs/arxiv_2025/PlanMoGPT_Flow-Enhanced_Progressive_Planning_for_Text_to_Motion_Synthesis.pdf
project_link: "https://PlanMoGPT.github.io"
code_link: null
aliases:
- PlanMoGPT
tags:
- arxiv_2025
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 渐进规划的多间隔计划采样（4帧、2帧、1帧）与流增强运动标记化（降低下采样率、扩大码本、流匹配解码器）。
primary_logic: 通过从粗到细的分层生成，LLM首先生成大间隔运动骨架（4帧计划），逐步细化至中等和完整序列，从而在保持全局语义的同时恢复细节；流匹配进一步补偿量化损失，实现高多样性和高质量生成。
claims:
- 在HumanML3D++长序列数据集上，FID从0.380（MoMask）降低到0.141，改善了63.8%。
- 多样性指标（MModality）在HumanML3D++上比MoMask提高了49.9%（2.538 vs 1.693）。
- 渐进规划消融实验表明，组合4帧和2帧计划同时改善了FID和R@1。
- 流增强VQ-VAE在全模型重建上达到FID 0.014，优于残差VQ-VAE的0.022。
---

# PlanMoGPT: Flow-Enhanced Progressive Planning for Text to Motion Synthesis

> [!tip] 核心洞察
> 通过从粗到细的分层生成，LLM首先生成大间隔运动骨架（4帧计划），逐步细化至中等和完整序列，从而在保持全局语义的同时恢复细节；流匹配进一步补偿量化损失，实现高多样性和高质量生成。

| 字段 | 内容 |
|------|------|
| 中文题名 | PlanMoGPT：面向文本到动作合成的流增强渐进规划 |
| 英文题名 | PlanMoGPT: Flow-Enhanced Progressive Planning for Text to Motion Synthesis |
| 会议/期刊 | arXiv 2025 |
| Links | [paper](https://arxiv.org/abs/2506.17912) · [Project](https://PlanMoGPT.github.io) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | PlanMoGPT |
| Dataset | HumanML3D++, KIT-ML++ |

> [!tip] 效果简介
> - HumanML3D++ 上，FID↓ 0.141 vs 0.380 (MoMask) (-63.8%)；MModality↑ 2.538 vs 1.693 (MoMask) (+49.9%)。
> - HumanML3D 上，R-Precision Top-1↑ 52.6% vs 52.2% (BAMM) (+0.4%)；MM-Dist↓ 2.884 vs 2.936 (BAMM) (-0.052)。
> - KIT-ML++ 上，FID↓ 0.230 vs 0.425 (MoMask) (-45.9%)。

## 概要

文本到动作生成的核心瓶颈在于**运动标记化的粒度困境**：细粒度标记使语言模型过度关注局部帧间连贯性，忽略长程语义对齐（局部依赖问题）；粗粒度标记虽利于全局规划，却丢失运动细节。PlanMoGPT 通过两个联动机制突破这一困境：

- **流增强运动标记器**：将下采样率从 4 降至 2、码本从 512 扩至 4096，并以流匹配解码器补偿量化损失，在保留时序分辨率的同时降低信息损耗。
- **渐进规划策略**：语言模型首先生成大间隔运动骨架（4 帧计划），再逐步细化为中粒度（2 帧计划）和完整序列，通过跨层注意力实现误差校正，兼顾全局语义与局部细节。

在 HumanML3D++ 长序列数据集上，PlanMoGPT 的 FID 从 MoMask 的 0.380 降至 **0.141**（改善 63.8%），多样性指标 MModality 从 1.693 提升至 **2.538**（提升 49.9%）。消融实验证实，组合多间隔计划同时改善 FID 和 R-Precision，流匹配解码器将重建 FID 从残差 VQ-VAE 的 0.022 进一步压缩至 0.014。

方法定位上，PlanMoGPT 属于**基于标记的自回归生成范式**，与 T2M-GPT（Zhang et al., CVPR 2023）、MoMask 等同属 LLM-based 路线，但通过流匹配与分层规划区别于扩散方法（MDM, Tevet et al., ICLR 2023; ReMoDiffuse, Zhang et al., ICCV 2023）和双向自回归方法（BAMM, Pinyoanuntapong et al., ECCV 2024）。在 KIT-ML 等低帧率数据集上表现相对受限，渐进规划的优势未能完全发挥。

### 文本到动作生成的核心挑战

文本到动作生成（Text-to-Motion Generation）旨在根据自然语言描述合成逼真的三维人体运动序列，在动画制作、虚拟人交互、游戏开发等领域具有广泛应用。近年来，基于大语言模型（LLM）的方法通过将连续运动离散化为“运动令牌”（motion tokens），将动作生成转化为序列预测任务，取得了显著进展。然而，这一范式面临一个根本性的瓶颈：**运动标记化的粒度困境**。

具体而言，细粒度标记化（高时间分辨率）能够保留丰富的运动细节，但会导致LLM在自回归生成时过度关注局部帧间连贯性，忽视全局语义对齐——即“局部依赖问题”（local dependency problem）。相反，粗粒度标记化虽有助于LLM把握整体运动结构，却不可避免地丢失大量细节信息，导致生成动作的保真度下降。这一粒度困境在长序列运动生成中尤为突出：序列越长，局部偏差的累积效应越严重，生成动作往往偏离文本语义，出现不自然的漂移或重复。

### 现有方法的局限

当前主流方法可大致分为扩散模型路线和LLM路线，但均未有效解决上述粒度困境：

- **扩散模型方法**（如 **MDM** (Tevet et al., ICLR 2023)、**MotionDiffuse**、**ReMoDiffuse** (Zhang et al., ICCV 2023)）直接在连续运动空间进行去噪生成，虽能保持较高的运动质量，但在长序列生成中计算成本高昂，且对文本语义的精确对齐能力有限。
- **LLM路线方法**（如 **T2M-GPT** (Zhang et al., CVPR 2023)、**MoMask**、**MotionGPT**）通过VQ-VAE将运动离散化后交由LLM自回归生成，在语义对齐上表现更优，但受限于标记化粒度：**T2M-GPT** 采用4倍下采样和512大小的码本，标记粒度较粗；**MoMask** 引入残差VQ-VAE进行多层量化，在一定程度上缓解了细节丢失，但其残差结构仍无法从根本上补偿量化误差。此外，这些方法均采用逐令牌自回归生成，缺乏对运动全局结构的显式建模，在长序列场景下FID高达0.380，多样性指标MModality仅1.693。

### 本文动机与核心思路

针对上述问题，本文提出 **PlanMoGPT**，通过两个核心创新突破粒度困境：

1. **流增强细粒度运动标记化（Flow-Enhanced Motion Tokenizer）**：将VQ-VAE的下采样率从常规的4降至2，码本尺寸从512扩大至4096（八倍），从而在离散化阶段保留更丰富的运动细节。为补偿细粒度量化带来的信息损失，引入流匹配解码器（Flow Matching Decoder），通过常微分方程（ODE）从粗量化输出逐步注入细节，逼近真实运动序列。

2. **渐进规划生成策略（Progressive Planning）**：改变传统的逐令牌生成模式，让LLM首先生成大间隔运动骨架（如每4帧一个令牌的 $M_{b;4}$ 计划），建立全局运动结构；随后逐步细化至中等粒度（2帧间隔的 $M_{b;2}$ 计划），最终生成完整序列。这种从粗到细的分层生成机制，使LLM能够在保持全局语义一致性的同时恢复局部细节，并通过跨层误差校正机制利用粗粒度计划监督细粒度生成。

实验表明，PlanMoGPT在长序列数据集HumanML3D++上将FID从0.380（MoMask）降至0.141，改善63.8%；多样性指标MModality从1.693提升至2.538，提高49.9%，显著突破了现有方法的性能上限。

## 核心方法与创新机理

PlanMoGPT 的核心创新并非单一技术的堆砌，而是针对“运动标记化粒度-生成策略”这一对矛盾的协同重构。其设计围绕两条相互耦合的主线展开：**流增强细粒度运动标记器**与**基于多间隔计划的渐进式LLM生成**，二者共同解决了现有方法中全局语义对齐与局部细节保真不可兼得的瓶颈。

### 瓶颈定位：标记化粒度的两难困境

文本到动作生成的现有方法普遍面临一个结构性矛盾。若采用细粒度标记（如逐帧编码），LLM在自回归生成时会过度关注局部帧间连贯性，导致长序列的全局语义漂移——即“局部依赖问题”。反之，若采用粗粒度标记以维持全局结构，则不可避免地丢失运动细节，造成生成结果平滑、多样性不足。PlanMoGPT 的设计正是为了打破这一困境：**通过分层生成策略，让LLM在粗粒度层面掌控全局结构，再逐步注入细节；同时通过流匹配补偿量化损失，确保细节不丢失。**

### 创新点一：流增强细粒度运动标记器

传统方法（如 **MoMask** 采用的残差VQ-VAE）通常使用下采样率 $r=4$ 和码本大小 $K=512$ 进行运动压缩，导致量化损失较大，重建质量受限。PlanMoGPT 对标记器进行了三项关键改动：

- **降低下采样率至 $r=2$**：将时间分辨率提高一倍，保留更丰富的运动细节。
- **扩大码本至 $K=4096$**：码本容量提升八倍，显著降低量化误差。
- **引入流匹配解码器**：在VQ-VAE解码端嵌入条件流匹配（Conditional Flow Matching），以ODE形式从粗量化输出逐步演化到真实运动序列。其核心公式为：

$$\frac{d y_t}{d t} = \mathbf{F}_{\theta}(y_t, t), \quad t \in [0, 1]$$

训练时，向量场 $\mathbf{F}_{\theta}$ 学习预测从当前状态 $y_t$ 到真实运动 $y_1$ 的最短路径切向量：

$$\mathcal{L}_{\mathrm{CFM}}(\theta) = \mathbb{E}_{t, y_1, y_t} \big\| \mathbf{F}_{\theta}(y_t, t) - u(y_t | y_1) \big\|^2$$

推理时通过离散化迭代细化：

$$y_{t_{i+1}} = y_{t_i} + \mathbf{F}_{\theta}(y_{t_i}, t_i) \cdot \Delta t, \quad 0 = t_0 < \dots < t_T = 1$$

这一设计的因果逻辑是：细粒度标记降低了编码端的信息损失，但解码端的重建压力随之增大；流匹配解码器恰好承担了这一压力，通过连续的向量场引导将粗量化结果“推”向高保真运动。消融实验证实了该设计的有效性：流增强VQ-VAE在全模型重建上达到 FID 0.014，优于残差VQ-VAE的 0.022（Table 7）；移除流匹配后，PlanMoGPT base 的生成 FID 从 0.048 退化至 0.106（Table 2）。

### 创新点二：渐进规划式LLM生成

传统LLM方法（如 **T2M-GPT**, Zhang et al., CVPR 2023）直接逐令牌生成完整运动序列，缺乏对全局结构的显式建模。PlanMoGPT 引入**多间隔计划采样**与**从粗到细的渐进生成**机制：

- **多间隔计划采样**：按间隔 $T$ 对运动令牌进行采样，构建多粒度计划骨架。公式为：

$$M_{b;T} = \{ m_{b+kT} \mid 0 \leq k \leq \lfloor (l - b) / T \rfloor \}$$

- **渐进生成序列**：LLM首先生成4帧间隔的全局运动骨架 $M_{b;4}$，再依次生成2帧间隔的中等计划 $M_{b;2}$ 和完整的1帧序列 $M$，形成分层生成序列：

$$U = [\mathbf{S}_4] \oplus M_{b;4} \oplus [\mathbf{S}_2] \oplus M_{b;2} \oplus [\mathbf{S}_1] \oplus M$$

这一策略的本质是将“全局结构规划”与“局部细节填充”解耦。LLM首先在高度压缩的粗粒度空间（4帧间隔）中建立运动的大尺度语义框架，随后在逐步细化的过程中，利用已生成的粗粒度计划作为跨层监督信号。实验观察到，跨注意力权重中 32.9% 和 15.3% 分别分配给 $M_{b;4}$ 和 $M_{b;2}$，表明粗粒度计划确实在细粒度生成中发挥了校正作用。

消融实验（Table 4）明确显示：单独使用4帧或2帧计划均不如组合计划，组合计划同时改善了 FID 和 R@1。这验证了多粒度层次之间的互补性——4帧计划提供全局约束，2帧计划作为中间桥梁，共同引导完整序列的生成。

### 创新协同：从矛盾到互补

两项创新的协同效应体现在：细粒度标记器提供了足够的细节容量，但若直接交由LLM逐令牌生成，仍会陷入局部依赖；渐进规划恰好将LLM的注意力引导至不同粒度的结构层次，使粗粒度令牌承载全局语义，细粒度令牌专注局部连贯。流匹配解码器则作为最后一道保障，将量化后的粗输出进一步精炼。这一“编码-规划-解码”三级协同设计，是PlanMoGPT在长序列生成上将FID从0.380（MoMask）降至0.141（改善63.8%）、同时将多样性指标提升49.9%的根本原因。

PlanMoGPT 采用两阶段流水线：**流增强运动标记器**与**集成渐进规划的 LLM**，前者将连续运动序列转换为细粒度离散令牌，后者以从粗到精的方式逐层生成令牌序列，最终由流匹配解码器恢复完整运动。

### 流水线概览

1. **运动编码与量化**：输入运动序列 $\boldsymbol{y} = \{p_i\}_{i=1}^n$（$p_i \in \mathbb{R}^{d_m}$ 为第 $i$ 帧的关节位姿向量）首先通过 VQ-VAE 编码器进行下采样，得到潜变量并量化为离散令牌。与先前工作相比，本方法将**下采样率从 4 降至 2**、**码本尺寸从 512 扩至 4096**，以保留两倍时序分辨率并降低量化损失。

2. **流增强解码**：量化后的粗运动 $y_0$ 作为初始条件，通过流匹配解码器沿 ODE 轨迹逐步细化：
   $$\frac{d y_t}{d t} = \mathbf{F}_{\theta}(y_t, t), \quad t \in [0, 1]$$
   推理时采用欧拉离散化迭代更新 $y_{t_{i+1}} = y_{t_i} + \mathbf{F}_{\theta}(y_{t_i}, t_i) \cdot \Delta t$，从粗量化输出逼近真实运动 $y_1$。向量场 $\mathbf{F}_\theta$ 由条件流匹配损失训练：
   $$\mathcal{L}_{\mathrm{CFM}}(\theta) = \mathbb{E}_{t, y_1, y_t} \big\| \mathbf{F}_{\theta}(y_t, t) - u(y_t | y_1) \big\|^2$$
   其中 $u(y_t|y_1)$ 表示 $y_t$ 到 $y_1$ 最短路径的切向量。

3. **渐进规划生成**：LLM（基于 TinyLLaMA）不直接逐令牌预测完整序列，而是按多间隔计划采样生成分层令牌序列：
   $$U = [\mathbf{S}_4] \oplus M_{b;4} \oplus [\mathbf{S}_2] \oplus M_{b;2} \oplus [\mathbf{S}_1] \oplus M$$
   其中 $M_{b;T} = \{ m_{b+kT} \mid 0 \leq k \leq \lfloor (l - b) / T \rfloor \}$ 为按间隔 $T$ 采样的运动令牌子序列，$\mathbf{S}_4$、$\mathbf{S}_2$、$\mathbf{S}_1$ 为特殊分隔令牌。LLM 首先生成 4 帧间隔的全局运动骨架 $M_{b;4}$，再依次细化为 2 帧间隔计划 $M_{b;2}$ 和完整序列 $M$。

4. **跨层误差校正**：粗粒度计划（$M_{b;4}$、$M_{b;2}$）通过交叉注意力机制为细粒度生成提供结构监督，注意力分配比例分别为 32.9% 和 15.3%，使 LLM 在细化过程中保持全局语义一致性。

### 模块关系与数据流

- **Flow-Enhanced Motion Tokenizer**（编码器 + 流匹配解码器）独立训练，负责运动与令牌之间的双向映射，为后续 LLM 提供高质量离散表示。
- **LLM with Progressive Planning** 接收文本嵌入与渐进计划令牌，自回归生成分层运动令牌序列。
- 生成的全序列令牌经 VQ-VAE 解码器还原为粗运动，再通过流匹配 ODE 推理注入高频细节，输出最终运动。

### 关键设计决策

| 设计槽位 | 基线做法 | PlanMoGPT 做法 | 依据 |
|---------|---------|---------------|------|
| 下采样率 | $r=4$ | $r=2$ | 保留两倍时序分辨率 |
| 码本大小 | $K=512$ | $K=4096$ | 八倍容量降低量化损失 |
| 运动解码器 | 普通 CNN 解码器 | 流匹配 ODE 解码器 | 补偿量化损失，恢复细节 |
| 生成策略 | 逐令牌自回归 | 多间隔渐进规划 | 解决局部依赖，保持全局语义 |
| 跨层监督 | 无 | 粗粒度计划交叉注意力 | 32.9%/15.3% 注意力分配 |

> **注意**：上述注意力分配比例（32.9%、15.3%）来自原文 Sec 3.3 的跨层误差校正分析，但原文未提供该统计的详细计算方式与方差，建议手动核实其稳健性。

PlanMoGPT 由两个协同模块构成：**流增强运动标记器**（Flow-Enhanced Motion Tokenizer）负责将连续运动序列压缩为细粒度离散令牌并高质量重建；**带渐进规划的 LLM**（LLM with Progressive Planning）则从粗到细地生成这些令牌序列，以同时保证全局语义对齐和局部细节保真。

### 流增强运动标记器

该模块解决的核心矛盾是标记化粒度与信息保真度之间的权衡。传统方法（如 T2M-GPT、MoMask）采用较高的下采样率和较小的码本，导致量化损失累积，丢失高频运动细节。PlanMoGPT 从三个维度重构了这一模块：

1. **细粒度编码**：将 VQ-VAE 编码器的下采样率从常规的 $r=4$ 降至 $r=2$，使时间分辨率翻倍。同时将码本尺寸从 $K=512$ 扩大至 $K=4096$（八倍），以容纳更丰富的运动模式并降低量化误差。

2. **流匹配解码器**：在量化后的粗运动 $y_0$ 与真实运动 $y_1$ 之间建立连续演化路径。具体而言，定义一个由向量场 $\mathbf{F}_\theta$ 引导的常微分方程：

   $$\frac{d y_t}{d t} = \mathbf{F}_{\theta}(y_t, t), \quad t \in [0, 1]$$

   其中 $y_t$ 表示从粗糙起点 $y_0$ 向真实运动 $y_1$ 演化的中间状态。训练时，通过条件流匹配损失迫使网络学习最短路径的切向量：

   $$\mathcal{L}_{\mathrm{CFM}}(\theta) = \mathbb{E}_{t, y_1, y_t} \big\| \mathbf{F}_{\theta}(y_t, t) - u(y_t | y_1) \big\|^2$$

   这里 $u(y_t|y_1)$ 是从 $y_t$ 指向 $y_1$ 的最优方向。该损失避免了扩散模型中复杂的噪声调度，直接回归确定性路径。

3. **推理迭代细化**：给定量化输出 $y_0$，通过离散化 ODE 逐步注入细节：

   $$y_{t_{i+1}} = y_{t_i} + \mathbf{F}_{\theta}(y_{t_i}, t_i) \cdot \Delta t, \quad 0 = t_0 < \dots < t_T = 1$$

   每一步沿向量场方向推进，最终 $y_1$ 逼近真实运动分布。消融实验证实，移除流匹配（PlanMoGPT base）会使 HumanML3D 上的 FID 从 0.048 退化至 0.106，验证了该模块的关键作用。

### 带渐进规划的 LLM 生成

该模块针对 LLM 在长序列生成中的**局部依赖问题**：逐令牌自回归生成时，模型过度关注相邻令牌的连贯性，忽略全局语义约束，导致动作与文本脱节。

**多间隔计划采样**是核心机制。给定完整运动令牌序列 $M$，按不同间隔 $T$ 抽取子序列形成计划：

$$M_{b;T} = \{ m_{b+kT} \mid 0 \leq k \leq \lfloor (l - b) / T \rfloor \}$$

其中 $b$ 为起始偏移，$l$ 为序列长度。PlanMoGPT 采用三层计划：$T=4$（稀疏骨架，捕获全局结构）、$T=2$（中等粒度过渡）、$T=1$（完整序列）。生成时，LLM 按以下分层序列逐段预测：

$$U = [\mathbf{S}_4] \oplus M_{b;4} \oplus [\mathbf{S}_2] \oplus M_{b;2} \oplus [\mathbf{S}_1] \oplus M$$

其中 $\mathbf{S}_4$、$\mathbf{S}_2$、$\mathbf{S}_1$ 为特殊分隔令牌，提示模型切换生成粒度。这一设计将生成过程从“逐令牌预测”转变为“结构化计划演进”：先确立大尺度运动骨架，再逐步填充细节。

**跨层误差校正**进一步强化了粗细粒度间的信息流动。在生成完整序列 $M$ 时，LLM 的交叉注意力会显式关注已生成的粗粒度计划——实验观测到 $M_{b;4}$ 和 $M_{b;2}$ 分别获得 32.9% 和 15.3% 的注意力权重，表明模型自发利用高层计划约束底层细节生成，有效抑制了误差累积。

消融实验（Table 4）证实，单独使用 4 帧或 2 帧计划均不如组合方案——组合计划同时改善了 FID 和 R-Precision Top-1，验证了多粒度分层生成的协同效应。

## 实验与关键发现

### 主实验结果

PlanMoGPT 在四个基准数据集上进行了系统评估，包括标准数据集 HumanML3D 和 KIT-ML，以及长序列扩展版本 HumanML3D++ 和 KIT-ML++。Table 2 汇总了 PlanMoGPT 与主流基线方法的对比结果。

![[assets/figures/papers/paper_list_l20_https_arxiv_org_abs_2506_17912/figures/004_Table_2.jpg]]
*Table 2: Comparing our PlanMoGPT with baselines on multiple datasets. Bold indicates the best result, and underlined indicates the second best result. § indicates using ground-truth motion length as extra information. PlanMoGPT (base) means using VQ-VAE without flow matching. Mo-Mask (Base) and BAMM (Base) refers to using residual VQ-VAE but without residual Transformer. We implement a variant version of the original T2M-GPT, denoted as T2M-GPT*, which only differs from PlanMoGPT (base) in that there is no progressive planning. MoMask and T2M-GPT are retrained by their source code on the HumanML3D++ and KIT-ML++ datasets*

在长序列数据集 **HumanML3D++** 上，PlanMoGPT 展现出显著优势：FID 达到 **0.141**，相比 MoMask 的 0.380 降低了 **63.8%**，验证了渐进规划机制在长序列生成中的核心价值。多样性指标 MModality 达到 **2.538**，较 MoMask 的 1.693 提升了 **49.9%**，表明流增强解码器有效补偿了量化损失，释放了生成多样性。R-Precision Top-1 达到 40.1%，同样优于所有对比方法。

在标准数据集 **HumanML3D** 上，PlanMoGPT 的 FID 为 **0.048**，R-Precision Top-1 为 **52.6%**，MM-Dist 为 **2.884**，三项指标均达到最优或次优水平。值得注意的是，PlanMoGPT 在未使用真实运动长度（§ 标注）的情况下，FID 已优于使用该额外信息的 ReMoDiffuse（0.103 vs 0.048），体现了方法自身对运动时长建模的鲁棒性。

在 **KIT-ML++** 长序列数据集上，FID 从 MoMask 的 0.425 降至 **0.230**（改善 45.9%），进一步验证了方法的跨数据集泛化能力。

**公平性说明**：所有对比方法在相同数据划分上重新训练（如适用），MoMask 和 T2M-GPT 在 HumanML3D++ 和 KIT-ML++ 上使用其源代码重新训练。PlanMoGPT 与基线使用相同的主干 LLM（TinyLLaMA）以确保公平比较。

---

### 消融实验

#### 流匹配解码器的有效性

Table 2 中 PlanMoGPT 与 PlanMoGPT (base) 的对比直接揭示了流匹配的贡献：在 HumanML3D 上，移除流匹配后 FID 从 0.048 退化至 **0.106**，M-Dist 从 2.884 恶化至 3.010。这表明 VQ-VAE 的量化损失在细粒度编码（r=2, K=4096）下仍然显著，而流匹配解码器通过 ODE 迭代细化有效补偿了该损失。

Table 7 进一步从重建角度验证了流增强 VQ-VAE 的优越性：在全模型配置下（codebook 4096, 下采样率 2），流增强 VQ-VAE 的重建 FID 为 **0.014**，优于残差 VQ-VAE 的 0.022。值得注意的是，残差 VQ-VAE 需要额外的残差令牌才能达到可比重建质量，而流增强版本在基础配置下即可实现更优重建。

![[assets/figures/papers/paper_list_l20_https_arxiv_org_abs_2506_17912/figures/013_Table_7.jpg]]
*Table 7: Reconstruction of our flow-enhanced VQ-VAE and residual VQ-VAE on the HumanML3D test dataset. “base” for “residual” refers to the motion is reconstructed by residual VQ-VAE without residual tokens; “base” for “Flow” refers to our VQ-VAE without flow matching method; “4096, 2” refers to the size of the codebook is 4096, and the downsampling rate is 2*

#### 渐进规划机制的分析

Table 4 对渐进规划策略进行了系统消融。核心发现包括：

![[assets/figures/papers/paper_list_l20_https_arxiv_org_abs_2506_17912/figures/008_Table_4.jpg]]
*Table 4: Analysis of progressive planning method based on the HumanML3D test dataset*

- **单独使用 4 帧计划**：FID 为 0.092，R@1 为 51.6%
- **单独使用 2 帧计划**：FID 为 0.088，R@1 为 51.4%
- **组合 4 帧 + 2 帧计划**：FID 改善至 **0.048**，R@1 提升至 **52.6%**

组合计划同时改善了生成质量和语义对齐，验证了从粗到细的分层生成策略的有效性。4 帧计划提供全局运动骨架，2 帧计划补充中等粒度细节，两者形成互补。

#### 标记化粒度的影响

Table 5(a) 展示了标记化粒度对 PlanMoGPT (base) 性能的影响。将码本尺寸从 512 增至 **4096**、下采样率从 4 降至 **2** 时，生成 R-Precision 持续提升，验证了细粒度标记化对语义保持的积极作用。然而，单独增加码本或降低下采样率均不足以完全解决局部依赖问题——这正是渐进规划机制的必要性所在。

![[assets/figures/papers/paper_list_l20_https_arxiv_org_abs_2506_17912/figures/010_Table_5.jpg]]
*Table 5: (a). The impact of granularity of motion tokenization to the PlanMoGPT (Base) on the HumanML3D test dataset*

---

### 失败模式与局限性

1. **低帧率数据集的适配性**：在 KIT-ML（12.5fps）上，PlanMoGPT 的 FID 改善幅度（45.9%）低于 HumanML3D++（63.8%）。低帧率导致帧间运动变化更大，渐进规划的多间隔采样可能无法充分捕获快速运动细节。Table 6 显示 KIT-ML 上的 R@1 为 41.2%，低于 BAMM 的 42.6%，提示需要针对低帧率场景调整计划间隔策略。

2. **流匹配推理的步数开销**：ODE 离散化步数 T 直接影响推理速度与质量的权衡。论文未详细报告不同步数下的 FID-延迟曲线，实际部署时需手动验证最优步数配置。

3. **跨层误差校正的隐式性**：论文报告了跨注意力权重分配（32.9% 给 4 帧计划，15.3% 给 2 帧计划），但该机制完全依赖 LLM 的注意力学习，缺乏显式约束。在极端长序列或复杂语义场景下，注意力分配可能失效，需进一步验证。

---

### 重要图表结论汇总

- **Table 2**：PlanMoGPT 在 HumanML3D++ 上 FID 0.141、MModality 2.538，均显著优于所有基线；在 HumanML3D 上 FID 0.048 达到最优。
- **Table 4**：组合 4 帧和 2 帧计划同时改善 FID 和 R@1，验证了渐进规划的核心设计。
- **Table 5(a)**：码本增大至 4096 且下采样率降至 2 持续提升生成 R-Precision。
- **Table 7**：流增强 VQ-VAE 重建 FID 0.014，优于残差 VQ-VAE 的 0.022，验证了流匹配在补偿量化损失中的关键作用。
- **Table 6**：KIT-ML 上 R@1 略低于 BAMM，提示低帧率场景下渐进规划的局限性。

![[assets/figures/papers/paper_list_l20_https_arxiv_org_abs_2506_17912/figures/009_Table.jpg]]
*Table: (a) Impact of granularity of motion tokenization. (b) Comparison of residual and flow-enhanced*

![[assets/figures/papers/paper_list_l20_https_arxiv_org_abs_2506_17912/figures/007_Figure_4.jpg]]
*Figure 4: Case study on HumanML3D and HumanML3D++ datasets. The score range in Figure (a) ranges from 1 to 5, where 1 means poor and 5 means perfect. Figure (b) compares PlanMoGPT and other methods (ground-truth) to which one generates better results*

## 定位与知识库关联

### 1. 与现有工作的关系

PlanMoGPT 位于文本到动作生成（Text-to-Motion Generation）的离散令牌（discrete token）方法线上，其直接前驱包括 **T2M-GPT**（Zhang et al., CVPR 2023）和 **MoMask**。这些方法共享“运动VQ-VAE + 自回归生成”的基本范式，但 PlanMoGPT 在两条关键路径上做出了结构性改进。

**与 T2M-GPT / MoMask 的关系**：T2M-GPT 首次将运动生成建模为GPT式的逐令牌预测，但其标准VQ-VAE使用r=4下采样率和512大小的码本，导致令牌粒度较粗，重建细节丢失；MoMask 引入残差VQ-VAE以分层恢复细节，但残差令牌的层级结构并未在生成端被显式利用。PlanMoGPT 从两个方向突破这一瓶颈：
- **标记化粒度**：将下采样率降至r=2、码本扩大至4096（8倍），使单层VQ-VAE即可承载更细粒度的运动信息，避免了残差层级联带来的累积误差。
- **生成策略**：不再逐令牌预测完整序列，而是采用渐进规划——先生成4帧间隔的全局骨架令牌，再依次生成2帧间隔和1帧间隔的细化令牌。这一设计直接针对LLM在长序列生成中的“局部依赖”问题：细粒度令牌使模型过度关注相邻帧的连贯性，而忽略全局语义对齐。

**与扩散/流匹配方法的关系**：**MDM**（Tevet et al., ICLR 2023）、**MotionDiffuse**、**ReMoDiffuse**（Zhang et al., ICCV 2023）等扩散方法在连续空间直接生成运动序列，避免了量化损失，但推理速度较慢且多样性控制依赖随机采样。**MFM** 将流匹配引入运动生成，在连续空间中实现高效采样。PlanMoGPT 的流增强解码器借鉴了这一思想，但将其应用于离散令牌框架的“后处理”阶段：从VQ-VAE的粗量化输出出发，通过ODE逐步注入细节。这种混合策略保留了离散令牌在LLM集成和可控生成上的优势，同时利用流匹配补偿量化损失。

**与LLM-based方法的关系**：**MotionGPT** 和 **MotionLLM**（Wu et al., ICLR 2025）探索了将运动视为语言、用LLM统一建模的路径。PlanMoGPT 同样基于LLM（TinyLLaMA），但核心创新不在多模态对齐，而在生成过程的结构化——通过多间隔计划采样将运动生成从“逐令牌预测”转变为“计划演化”。这与 **BAMM**（Pinyoanuntapong et al., ECCV 2024）的双向自回归思路形成互补：BAMM 关注解码顺序的灵活性，PlanMoGPT 关注生成粒度的层次性。

### 2. 适用边界

PlanMoGPT 的设计假设和实验覆盖范围定义了其适用边界：

- **序列长度**：渐进规划的优势在长序列上最为显著。在 HumanML3D++（平均时长约10秒，远长于标准HumanML3D）上，FID 从 MoMask 的 0.380 降至 0.141（降幅63.8%），而在标准 HumanML3D 上 FID 为 0.048，与 BAMM 等方法的差距较小。这表明当序列较短时，全局结构的重要性降低，渐进规划的边际收益递减。
- **帧率与数据规模**：在 KIT-ML（12.5fps，规模较小）上，PlanMoGPT 的 FID 为 0.230，虽优于 MoMask 的 0.425，但论文明确指出“表现不如在 HumanML3D 上理想，因渐进规划可能受限”。低帧率意味着4帧间隔已覆盖0.32秒，粗粒度计划可能无法充分捕捉运动语义。
- **运动复杂度**：流增强解码器在重建指标上表现出色（全模型重建 FID 0.014 vs 残差VQ-VAE 0.022），但其增量细化能力受限于初始量化输出的质量。对于包含极端姿态或快速切换的运动，VQ-VAE 的量化损失可能超出流匹配的补偿范围。

### 3. 局限与开放问题

**已知局限**：
1. **低帧率/小数据集的退化**：如 KIT-ML 上的表现所示，渐进规划的有效性依赖于足够的帧率和数据量来支撑多粒度计划的语义意义。
2. **规划粒度的固定性**：当前方法使用固定的{4帧, 2帧, 1帧}三级规划，无法根据运动内容自适应调整。对于缓慢运动，4帧间隔可能过于稀疏；对于快速运动，2帧间隔可能仍不够细。
3. **流匹配的计算开销**：ODE推理需要多次前向传播（论文未明确报告推理步数），在实时应用中可能成为瓶颈。

**开放问题**：
1. **扩展到面部和手部运动**：论文明确将“生成包含面部表情和手部动作的运动”列为开放问题。这需要处理更高维度的姿态空间和更精细的局部依赖关系，可能要求规划粒度进一步细化或引入分区域规划。
2. **灵活的关键帧规划**：论文提出“手动选择关键帧”作为未来方向。当前的多间隔计划采样是均匀采样的，若能允许用户或高层控制器指定关键帧位置，将大幅提升交互式应用的可控性。
3. **规划层级的理论分析**：跨层误差校正的注意力分配（32.9%给4帧计划，15.3%给2帧计划）是观察性结果，缺乏对“为何这一比例最优”的理论解释。不同任务或数据集可能需要不同的注意力分配策略。

### 4. 知识库定位

PlanMoGPT 的核心贡献在于揭示了**运动标记化粒度与生成策略之间的耦合关系**：细粒度令牌需要分层生成策略来维持全局语义，而分层生成又需要流匹配来补偿细粒度令牌的量化损失。这一“粒度-规划-补偿”三角关系为离散令牌方法线提供了新的设计框架。

在更广的视野中，PlanMoGPT 代表了**离散令牌方法与连续生成方法的融合趋势**——用VQ-VAE的离散令牌保证LLM兼容性和可控性，用流匹配的连续细化保证生成质量。这一范式可迁移到其他需要“全局结构+局部细节”的序列生成任务（如音乐、语音手势）。

## 原文 PDF

![[paperPDFs/arxiv_2025/PlanMoGPT_Flow-Enhanced_Progressive_Planning_for_Text_to_Motion_Synthesis.pdf]]

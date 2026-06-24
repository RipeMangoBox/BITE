---
title: "LiveGesture: Streamable Co-Speech Gesture Generation Model"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/LiveGesture_Streamable_Co_Speech_Gesture_Generation_Model.pdf
project_link: "https://m-usamasaleem.github.io/publication/LiveGesture/LiveGesture.html"
code_link: null
aliases:
- LiveGesture
tags:
- CVPR_2026
- topic/generative_models_diffusion
- topic/benchmarks_datasets_evaluation
- topic/generative_models_diffusion/diffusion_image_video
core_operator: LiveGesture 的核心机制是严格因果（causal）的分层自回归架构：基于流式向量量化运动分词器（SVQ）将连续运动转换为因果离散词元，利用区域专家（xAR）建模各身体部位的局部运动动态，再通过因果时空融合模块（xAR-Fusion）捕获全身协调，并通过不确定性引导的掩码训练（UGM）缓解流式误差，从而在零前瞻约束下实现低延迟、节拍同步的实时手势生...
primary_logic: 通过将全身运动分解为分区域的离散词元，并采用两阶段因果训练（先区域专家后全局融合）结合混合掩码策略，即使在严格零前瞻约束下，模型也能匹配甚至超越离线方法的手势真实感和节拍同步性，证明了流式生成可以同时实现低延迟和高水平动作质量。
claims:
- LiveGesture 是唯一支持零前瞻流式生成的方法，在 BEAT2 数据集上取得最佳节拍一致性 BC=0.794、最高多样性 Div=13.91，且 FGD=4.57 接近离线最佳。
- 消融实验表明，移除因果时间注意力导致 FGD 从 4.57 升至 15.52，BC 从 0.794 降至 0.712，证实因果时空建模对全身协调至关重要。
- 在用户研究中，LiveGesture 取得最高的语音-手势同步性 MOS 评分 4.3，超越所有离线基线，表明其在节拍跟随和韵律捕获上的优势。
- BEAT2 上 FGD (↓) = 4.57
---

# LiveGesture: Streamable Co-Speech Gesture Generation Model

> [!tip] 核心洞察
> 通过将全身运动分解为分区域的离散词元，并采用两阶段因果训练（先区域专家后全局融合）结合混合掩码策略，即使在严格零前瞻约束下，模型也能匹配甚至超越离线方法的手势真实感和节拍同步性，证明了流式生成可以同时实现低延迟和高水平动作质量。

| 字段 | 内容 |
|------|------|
| 中文题名 | LiveGesture：可流式语音驱动全身手势生成模型 |
| 英文题名 | LiveGesture: Streamable Co-Speech Gesture Generation Model |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2604.10927) · [Project](https://m-usamasaleem.github.io/publication/LiveGesture/LiveGesture.html) |
| Topic | #topic/generative_models_diffusion #topic/benchmarks_datasets_evaluation #topic/generative_models_diffusion/diffusion_image_video |
| Method | LiveGesture |
| Dataset | BEAT2, User Study |

> [!tip] 效果简介
> - BEAT2 上，FGD (↓) 4.57 vs 4.25 (GestureLSM, offline best) (+0.32)；Beat Constancy (BC, →) 0.794 vs 0.781 (MambaTalk, offline best) (+0.013)；Diversity (↑) 13.91 vs 13.76 (GestureLSM, offline best) (+0.15)。
> - User Study (MOS, 1-5) 上，Speech-Gesture Synchrony (↑) 4.3 vs 4.1 (GestureLSM, offline best) (+0.2)。

## 概述

协语音手势生成旨在从语音信号中合成与说话人韵律、语义同步的全身动作，是虚拟人交互、数字孪生和具身对话代理的核心技术。然而，现有方法——包括 **HA2G**、**DisCo**、**CaMN**、**TalkShow**、**DiffSHEG**、**ProbTalk**、**EMAGE**、**MambaTalk**、**SynTalker**、**RAG-Gesture** 及当前离线最优的 **GestureLSM**——均采用离线设计，必须获取完整语音输入后才能生成手势，无法支持零前瞻（zero look-ahead）的实时流式推理。同时，多数方法将身体各区域独立建模或全局纠缠，未能捕获细粒度的区域间因果协调，导致高延迟且难以部署于真实交互场景。

**LiveGesture** 是首个严格因果、零前瞻的流式全身手势生成模型。其核心机制可概括为“分层因果自回归 + 流式向量量化”：通过**流式非对称运动分词器（SVQ）**将连续运动转换为区域特定的离散词元，再以**区域专家自回归变换器（xAR）**独立建模各身体部位的局部动态，最终由**因果时空融合模块（xAR-Fuse）**捕获全身协调关系，配合**不确定性引导掩码（UGM）**缓解流式预测的误差积累。这一设计使得模型在仅依赖过去和当前声学证据的条件下，实现每 200 ms 语音块低于 50 ms 的生成延迟。

在 BEAT2 数据集上，LiveGesture 作为唯一严格流式方法，取得了最佳节拍一致性（BC=0.794）、最高多样性（Div=13.91），且 FGD=4.57 接近离线最优。用户研究进一步表明，其语音-手势同步性的 MOS 评分（4.3/5）超越所有离线基线。消融实验证实：移除因果时间注意力导致 FGD 从 4.57 飙升至 15.52，BC 降至 0.712；关闭不确定性引导掩码使 BC 降至 0.723；组合式分区域 SVQ 分词器相较全身单一分词器在 FGD、BC 和多样性上均有显著优势。这些证据共同证明，流式生成在严格零前瞻约束下可以同时实现低延迟和高水平动作质量，为实时交互虚拟人提供了可行路径。

## 背景与动机

### 问题背景

在虚拟人、具身对话代理和沉浸式交互等应用中，语音驱动的全身手势生成是构建自然非言语行为的关键技术。人类在说话时会自发地协调身体各部位——躯干、手臂、手掌和面部——形成与语音韵律、语义高度同步的连贯动作。然而，现有协语音手势生成方法几乎全部采用**离线（offline）设计**：模型需要访问完整的语音输入后才能生成整个动作序列。这一假设从根本上限制了它们在真实交互场景中的可用性。

真实的人机对话是**流式（streaming）**的：语音以连续音频块的形式实时到达，虚拟人必须在仅知晓过去和当前声学证据的条件下，以极低延迟预测下一帧全身姿态。这种**零前瞻（zero look-ahead）**约束对模型架构提出了根本性挑战——任何依赖未来帧的编码器、注意力机制或后处理步骤都将导致不可接受的延迟，使系统无法部署。

### 现有方法的瓶颈

当前协语音手势生成领域存在两个相互交织的核心瓶颈：

**瓶颈一：离线范式与实时需求的根本矛盾。** 主流方法——包括基于VAE的**HA2G**、扩散模型**DiffSHEG**、自回归模型**EMAGE**和**MambaTalk**等——在训练和推理阶段均可访问完整语音话语。这些方法通常采用双向时间编码器或全局注意力，天然依赖未来上下文来提升动作质量。当试图将其改造为流式模型时，简单的因果掩码替换会导致性能急剧退化，因为模型失去了对未来韵律线索的利用能力。据我们所知，在LiveGesture之前，**没有任何方法能够在严格的零前瞻约束下生成高质量的全身手势**。

**瓶颈二：身体区域间协调建模不足。** 许多现有方法将全身运动作为一个整体进行全局建模，忽略了不同身体区域（上半身、下半身、双手、面部）在运动动态和节拍响应上的本质差异。另一些方法虽对各区域独立建模，却缺乏有效的区域间因果协调机制，导致生成的全身动作在时空上不协调——例如，手臂的节拍性动作与躯干的韵律摆动脱节。这种粗粒度的建模方式在离线场景下尚可通过全局注意力弥补，但在流式场景下，区域间的因果协调必须显式设计。

### 核心挑战与本文动机

上述瓶颈揭示了流式协语音手势生成的核心科学问题：**能否在严格零前瞻的因果约束下，同时实现低延迟、高节拍同步性和全身协调的实时手势生成？**

这一问题的难点在于三重权衡：

1. **因果性与质量**：不访问未来帧意味着模型必须在信息不完整的条件下做出预测，传统上这会导致动作真实感（以FGD衡量）和节拍一致性（以Beat Constancy衡量）的显著下降。
2. **区域专门化与全局协调**：各身体部位对语音的响应模式不同——手部动作更精细且语义性强，躯干运动更缓慢且与韵律包络相关——需要专门的局部建模，但同时又必须保证全身动作的时空一致性。
3. **流式误差累积**：自回归生成中，早期步骤的预测误差会沿时间步传播并放大，在流式场景下这一问题更为严重，因为模型无法通过未来帧进行纠偏。

LiveGesture的动机正是直面这三重挑战：通过**分层因果自回归架构**——将全身运动分解为分区域的离散词元，先由区域专家独立建模局部动态，再通过因果时空融合模块捕获全身协调——并结合**不确定性引导的掩码训练策略**来缓解流式误差，首次证明了流式手势生成可以在节拍同步性和多样性上匹配甚至超越离线方法。

## 核心创新

LiveGesture 的核心创新在于，它是在严格**零前瞻（zero look-ahead）**的流式约束下，首个能够生成高质量、节拍同步的全身协同语音手势的模型。其关键突破在于将离线手势生成的“全局双向建模”范式，彻底重构为“因果分层自回归”范式，从而解决了现有方法无法应用于实时交互场景的根本瓶颈。具体而言，其创新体现在以下四个紧密耦合的“changed slots”上。

### 1. 因果流式运动分词器（Streamable Motion Tokenizer）

**基线方案**：现有方法普遍采用双向（非因果）的 VQ-VAE 分词器，解码时依赖未来帧信息，无法支持流式生成。

**LiveGesture 的创新**：提出了非对称流式架构的 **SVQ（Streamable Vector-Quantized）分词器**。其核心设计是“双向编码器 + 严格因果解码器”的组合：编码器利用双向信息将原始运动序列压缩为低采样率的潜在序列，而解码器则仅依赖过去和当前的潜在状态进行重建。在此基础上，为每个身体区域（上半身、下半身、手部、面部）引入独立的码本进行向量量化，将连续运动转化为**因果离散运动词元**。这一设计使得运动生成从根本上摆脱了对未来信息的依赖，为真正的零前瞻流式解码铺平了道路。

**证据支撑**：消融实验（Appendix Table 6）证实，这种组合式分区域分词器显著优于全身单一分词器，FGD 从 6.84 降至 4.57，BC 从 0.753 升至 0.794，证明了区域专门化与因果设计的协同效应。

### 2. 分层自回归模型：从局部专家到全局因果融合

**基线方案**：许多方法将全身运动作为一个整体建模，或独立建模各区域但缺乏区域间的因果协调机制，导致动作僵硬或失去全身协调性。

**LiveGesture 的创新**：构建了**分层自回归模型（HAR）**，将全身手势生成分解为“局部动态学习”与“全局因果时空融合”两个阶段。
*   **区域专家（xAR）**：为每个身体区域设计独立的因果 Transformer，仅基于该区域的运动历史和当前音频，自回归地学习局部的节奏和表达动态。
*   **因果时空融合（xAR-Fuse）**：冻结区域专家后，引入一个全局融合 Transformer。它通过**因果交叉注意力**接收各区域专家的隐藏状态（经由轻量级 PILOR 适配器对齐），并执行**全局因果时间注意力**和**区域间空间注意力**，从而在严格不访问未来信息的约束下，显式地捕获全身各部位之间的实时协调关系。

**证据支撑**：消融实验（Table 2a, 2b）是该创新的决定性证据。移除融合模块中的因果时间注意力，导致 FGD 从 4.57 急剧恶化至 15.52，BC 从 0.794 降至 0.712。仅使用区域专家而不进行融合，FGD 为 6.458；加入 xAR-Fuse 后 FGD 降至 4.57。这有力地证明了因果时空融合是全身协调生成的核心机制。

### 3. 面向流式误差的混合掩码训练策略

**基线方案**：标准训练采用教师强制（teacher forcing），不考虑流式场景下自回归预测误差的累积效应，导致开环推理时性能急剧下降。

**LiveGesture 的创新**：设计了两阶段训练与混合掩码策略以缓解流式误差。
*   **不确定性引导的词元掩码（UGM）**：在融合训练阶段，根据模型对各区域下一词元预测的不确定性，动态地、概率性地用真实词元替换被掩码的词元。这模拟了流式推理中可能出现的错误模式，迫使模型学会从有噪声的历史中进行鲁棒预测。
*   **随机区域掩码（RM）**：随机掩盖整个区域的运动词元，强制模型利用其他区域的信息进行推断，增强了模型对部分信息缺失的鲁棒性。
*   **分类器自由引导（CFG）**：在推理时，通过组合条件与无条件 logits 来强化音频/文本对齐，进一步补偿流式场景下的对齐漂移。

**证据支撑**：关闭 UGM 导致 BC 从 0.794 降至 0.723，FGD 升至 4.98（Table 2a），证实该训练策略对缓解流式误差积累至关重要。

### 4. 因果可流式音频编码器

**基线方案**：离线音频编码器可访问完整话语，提取全局声学特征。

**LiveGesture 的创新**：设计了基于因果卷积和扩张金字塔的**流式音频编码器**。它仅使用左侧填充，从第一层即强制执行因果性，确保每一步仅依赖过去和当前的声学证据，为自回归模型提供严格对齐的、无未来信息的音频词元。这使得整个系统从音频输入到运动生成的管线实现了端到端的因果性。

**总结**：LiveGesture 的创新并非单一技术的堆砌，而是一套完整的系统级重构。通过将“因果性”注入到分词、局部建模、全局融合、音频编码乃至训练策略的每一个环节，它首次证明了在零前瞻的严格约束下，流式手势生成模型能够匹配甚至超越离线方法的动作质量与节拍同步性。

## 整体框架

LiveGesture 是一个严格因果（causal）、零前瞻（zero look-ahead）的流式协语音手势生成系统。给定实时音频流（以及可选的在线文本转录），系统逐帧预测 SMPL-X 全身姿态参数，每 200 ms 音频块的推理延迟低于 50 ms，无需等待完整话语即可输出连贯、节拍同步的手势（Figure 1）。

![[assets/figures/papers/paper_list_l993_https_arxiv_org_abs_2604_10927/figures/001_Figure_1.jpg]]
*Figure 1: LiveGesture overview. Given live audio chunks, our framework generates full-body SMPL-X motion online with zero lookahead. A streamable SVQ motion tokenizer and a hierarchical eXpert-fused autoregressive model (region-wise AR eXperts plus causal spatial–temporal fusion) enable low-latency (\< 50 ms per 200 ms chunk) generation of diverse, beat-synchronous gestures over arbitrarylength speech, in contrast to prior offline gesture methods that require full utterances and incur much higher latency*

整个 pipeline 由两大核心模块串联构成：

1. **流式向量量化运动分词器（Streamable Vector-Quantized Motion Tokenizer, SVQ）**：将每个身体区域的连续运动序列压缩为低采样率的离散运动词元（motion token），并保证解码过程严格因果，为下游自回归生成提供紧凑、可流式的符号化表示。
2. **分层自回归 Transformer（Hierarchical Autoregressive Transformer, HAR）**：以因果方式接收音频/文本词元，先由四个区域专家（Region-eXperts, xAR）独立建模各身体部位的局部运动动态，再通过因果时空融合模块（xAR-Fusion）捕获全身协调关系，最终预测下一帧的运动词元。

### 输入输出流

在时刻 $t$，模型的输入仅包含：
- 最近的运动历史 $\mathbf{S}_t$（已生成的姿态序列），
- 当前因果音频词元 $a_t$（由流式音频编码器实时提取），
- 可选的在线文本词元 $w_t$。

模型输出下一帧的全身姿态预测：

$$\hat{\mathbf{q}}_t = f_{\Theta}(\mathbf{S}_t, a_t, w_t)$$

该公式明确体现了“零前瞻”约束：预测完全基于过去和当前信息，不访问任何未来帧。

### 模块间关系

两个核心模块的协作流程如下：

1. **SVQ 分词器**（Figure 2）采用非对称架构——双向编码器 + 因果解码器，先将各区域的原始运动序列降采样 4 倍得到潜在序列 $z^{\mathrm{region}}$，再通过区域特定码本量化为离散词元。解码端仅依赖已生成的词元，保证流式兼容。
2. **HAR 模型**（Figure 3）以冻结的 SVQ 词元为预测目标。流式音频编码器（基于因果卷积和扩张金字塔）提供与运动词元时间对齐的音频词元；四个区域专家分别以因果自回归方式建模上体、下体、手部、面部的局部动态；各专家的隐藏状态经轻量残差适配器（PILOR）映射到共享融合空间后，由 xAR-Fusion 通过因果交叉注意力与时空注意力捕捉全身协调，最终由词元分类器预测下一帧各区域的运动词元。
3. **训练策略**分为两阶段：第一阶段训练区域专家学习局部自回归动态，注入高斯噪声以增强鲁棒性；第二阶段冻结区域专家，训练融合 Transformer，采用不确定性引导的词元掩码（UGM）和随机区域掩码（RM）缓解流式误差积累。推理时通过分类器自由引导（CFG）进一步增强音画同步。

这一分层因果设计使得 LiveGesture 成为目前唯一在严格零前瞻约束下运行，且在节拍一致性（BC=0.794）和多样性（Div=13.91）上超越离线方法的流式手势生成系统。

## 核心模块与公式推导

LiveGesture 由两大因果模块级联构成：**流式向量量化运动分词器（SVQ）** 与 **分层自回归 Transformer（HAR）**，二者在严格零前瞻约束下协同工作。整体生成范式可表述为：

$$\hat{\mathbf{q}}_t = f_{\Theta}(\mathbf{S}_t, a_t, w_t)$$

其中，在时刻 $t$，模型仅依据最近的局部运动历史 $\mathbf{S}_t$、当前因果音频词元 $a_t$ 及可选文本词元 $w_t$，预测下一帧全身 SMPL-X 姿态 $\hat{\mathbf{q}}_t$，全程不访问未来帧。

### 3.1 流式非对称运动分词器（SVQ）

SVQ 的核心设计目标是将连续运动序列压缩为**因果可解码的离散词元**。针对每个身体区域（上半身、下半身、双手、面部），分词器采用非对称架构：

- **双向编码器**：将原始帧率运动序列 $\{\theta_{t}^{\text{region}}\}_{t=1}^{T_f}$ 投影到低采样潜在空间，得到 $z^{\text{region}} = \{z_{\tau}\}_{\tau=1}^{T}$，其中 $T = T_f / 4$，即 4 倍降采样。
- **因果解码器**：仅依赖当前及过去潜在帧进行重建，确保流式解码可行性。
- **区域特定码本与投影头**：冻结自编码器后，第二阶段仅优化码本 $\{e^{\text{region}}\}$ 和投影头 $W^{\text{region}}$，损失函数为：

$$\mathcal{L}_{\text{stage2}} = \lambda_{\text{rec}} \big\| \theta^{\text{region}} - D_{\text{CS}}\big( W^{\text{region}}(\hat{z}^{\text{region}}) \big) \big\|_1 + \lambda_{\text{cb}} \mathcal{L}_{\text{cb}}(z^{\text{region}}, e^{\text{region}})$$

该设计使每个区域获得专属的离散运动词元流，且所有词元在时间上严格对齐，为后续分层自回归建模奠定基础。

### 3.2 分层自回归模型（HAR）

HAR 采用“先局部后全局”的两级因果架构，由区域专家、因果时空融合模块和流式音频编码器三部分组成。

#### 3.2.1 区域专家（xAR）

每个身体区域 $r \in \mathcal{R}$ 拥有独立的因果自回归 Transformer，建模其音频驱动的局部运动动态：

$$p_{\phi}^r ( x_{1:T}^r \mid a_{1:T}, w_{1:T} ) = \prod_{t=1}^{T} p_{\phi}^r \big( x_t^r \mid x_{1:t-1}^r, a_{1:t}, w_{1:t} \big)$$

其中 $x_t^r$ 为区域 $r$ 在时刻 $t$ 的 SVQ 运动词元，预测仅依赖该区域的历史词元和当前因果音频/文本条件。区域专家独立捕获各部位的节奏与表达特征，专家间不直接通信。

#### 3.2.2 因果时空融合（xAR-Fuse）

融合模块接收所有冻结的区域专家隐藏状态，通过**预注入适配器（PILOR）** 将异构表示映射到共享空间：

$$\Delta h_t^r = \mathscr{W}_r h_t^r, \quad \tilde{h}_t^r = h_t^r + \Delta h_t^r$$

其中 $\mathscr{W}_r$ 为区域 $r$ 的轻量残差投影矩阵。适配后的隐藏状态进入因果时空 Transformer，依次执行：

- **因果音频-运动交叉注意力**：将音频条件显式注入各区域表示；
- **全局因果时间注意力**：沿时间轴建模全身运动的时序依赖；
- **区域间空间注意力**：捕获同一时刻不同身体部位的协调关系。

最终，词元分类器输出下一时刻各区域的离散运动词元预测。

#### 3.2.3 流式音频编码器

音频编码器基于因果一维卷积和扩张金字塔结构，仅使用左侧填充（left-only padding）从第一层即强制因果性。它以实时音频块为输入，输出与运动词元采样率严格对齐的因果音频词元序列，参数规模约 0.5M。

### 3.3 两阶段因果训练策略

**第一阶段**：独立训练各区域专家，使用标准自回归交叉熵损失：

$$\mathcal{L}_{\text{local}} = - \sum_{r \in \mathcal{R}} \sum_{t=1}^{T} \log p_{\phi}^r \big( x_t^r \mid x_{1:t-1}^r, a_{1:t}, w_{1:t} \big)$$

同时向局部专家注入高斯噪声以模拟流式预测的误差累积。

**第二阶段**：冻结区域专家，训练融合 Transformer。采用**混合掩码策略**——不确定性引导的词元掩码（UGM）按余弦退火调度选择性地掩盖高不确定度区域，结合随机区域掩码（RM）迫使模型学习跨区域协调。融合损失为：

$$\mathcal{L}_{\text{fuse}} = - \sum_{t=1}^{T} \sum_{r \in \mathcal{M}_t} \log p_{\theta} \left( x_t^r \mid \tilde{x}_{1:t}^{1:|\mathcal{R}|}, a_{1:t}, \tilde{w}_{1:t} \right)$$

其中 $\mathcal{M}_t$ 为时刻 $t$ 被掩盖的区域集合。

推理时，采用**分类器自由引导（CFG）** 增强音画同步性。训练阶段以一定概率随机丢弃音频、文本或两者，使模型学习无条件先验；推理时将条件与无条件 logits 按比例组合：

$$\ell_{\text{guided}}^r = \ell_{\text{uncond}}^r + \gamma (\ell_{\text{cond}}^r - \ell_{\text{uncond}}^r)$$

其中 $\gamma \ge 1$ 为引导强度，消融实验表明 $\gamma = 1.25$ 时性能最优。

### 补充图表

![[assets/figures/papers/paper_list_l993_https_arxiv_org_abs_2604_10927/figures/002_Figure.jpg]]
*Figure: Streamable Asymmetric Motion Tokenizer*

![[assets/figures/papers/paper_list_l993_https_arxiv_org_abs_2604_10927/figures/003_Figure_3.jpg]]
*Figure 3: Overview of the Hierarchical Autoregressive Model in LiveGesture. A streamable audio encoder and optional text encoder provide causal audio/text tokens to four local AR Region-eXperts (upper body, lower body, hands, face), each modeling its own SVQ motion token stream. Their frozen states are adapted by per-region Pre-Infusion Adapters (PILOR) and fused by xAR-Fuse, a causal spatial–temporal transformer with audio–motion cross-attention, global temporal attention, and inter-region spatial attention that predicts next-step SVQ tokens for zero–look-ahead streaming full-body gesture generation*

## 实验与分析

### 主实验结果

LiveGesture 在 BEAT2 数据集上与 11 个离线方法进行了全面比较，是**唯一支持零前瞻流式生成**的模型。Table 1 报告了包含面部运动模块的完整结果。

![[assets/figures/papers/paper_list_l993_https_arxiv_org_abs_2604_10927/figures/005_Table_1.jpg]]
*Table 1: State-of-the-art comparison on BEAT. Best results are shown in bold and second best are underlined. The Streaming column indicates whether the method supports zero-look-ahead streaming (✓) or is offline-only (✗); Our method is the only streaming model while remaining superior in most of important metrics*

![[assets/figures/papers/paper_list_l993_https_arxiv_org_abs_2604_10927/figures/011_Table_1.jpg]]
*Table 1: Comparison with state-of-the-art methods on BEAT2 without the facial motion module. LiveGesture remains the only zero–lookahead streaming model while achieving competitive or superior performance in BC and Diversity*

**定量对比**：LiveGesture 在多个关键指标上匹配甚至超越离线最优方法：
- **节拍一致性（BC）**：0.794，超越离线最优 MambaTalk 的 0.781，表明流式因果设计能更精准地跟随语音节奏。
- **多样性（Div）**：13.91，超越离线最优 GestureLSM 的 13.76，证明零前瞻约束并未损害动作丰富度。
- **FGD**：4.57，略逊于离线最优 GestureLSM 的 4.25（差距 +0.32），这是无法访问未来帧的必然代价。
- **面部 MSE**：1.241，弱于 GestureLSM 的 1.021，面部逼真度仍有提升空间。

在不包含面部模块的对比中（Appendix Table 1），LiveGesture 同样保持 BC 和 Div 的竞争力，进一步验证了流式因果设计的有效性。

**用户研究**：在 BEAT2 测试片段上的 MOS 评分（Appendix Table 2）显示，LiveGesture 在**语音-手势同步性**上获得最高分 4.3，超越所有离线基线（包括 GestureLSM 的 4.1），表明人类观察者能明显感知到其节拍跟随和韵律捕获的优势。在真实感和平滑度上，LiveGesture 也保持竞争力。

**延迟性能**：LiveGesture 在每 200 ms 音频块上实现 < 50 ms 的推理延迟，首帧延迟约 250 ms，满足实时交互需求。相比之下，离线方法需要完整语音输入后才能生成，延迟随话语长度线性增长。

### 消融实验

Table 2 系统消融了 LiveGesture 的核心设计选择，揭示了各组件对性能的因果贡献。

![[assets/figures/papers/paper_list_l993_https_arxiv_org_abs_2604_10927/figures/007_Table_2.jpg]]
*Table 2: Ablation studies of LiveGesture design choices, including core components, architecture, tokenization, audio encoders, loss weights, and UGR*

![[assets/figures/papers/paper_list_l993_https_arxiv_org_abs_2604_10927/figures/012_Table_2.jpg]]
*Table 2: Mean Opinion Scores (MOS, 1–5, higher is better) from the user study on BEAT2 test clips. The Streaming column indicates whether the method supports zero–look-ahead streaming (✓) or is offline-only (✗). LiveGesture is the only strictly streaming model and is preferred on speech–gesture synchrony while remaining competitive in realness and smoothness*

**核心组件消融**（Table 2a）：
- **移除融合时间注意力**：FGD 从 4.57 急剧上升至 15.52，BC 从 0.794 降至 0.712。这证实因果时空建模是全身协调的**决定性瓶颈**——没有时间注意力，模型无法有效融合各区域的时序动态。
- **关闭不确定性引导掩码（UGM）**：BC 降至 0.723，FGD 升至 4.98。UGM 通过优先掩码高不确定性词元，有效缓解了流式预测中的误差积累问题。
- **移除区域随机掩码（RM）**：FGD 升至 4.82，BC 降至 0.762。RM 通过随机掩码区域增强融合模型的鲁棒性。

**分层架构消融**（Table 2b）：
- **仅使用区域专家（xAR）而不进行因果融合**：FGD 为 6.458，BC 为 0.762。添加 xAR-Fuse 后 FGD 降至 4.57，BC 升至 0.794。这证明区域专家能捕获局部动态，但**全局协调必须依赖融合模块**。
- **因果交叉注意力 vs 因果自注意力**（Appendix Table 4）：FGD 4.57 vs 4.63，BC 0.794 vs 0.784。显式的跨模态交叉注意力路径优于将音频和运动简单拼接的自注意力融合。

![[assets/figures/papers/paper_list_l993_https_arxiv_org_abs_2604_10927/figures/014_Table_4.jpg]]
*Table 4: Comparison of causal self-attention and causal audio–motion cross-attention in the Hierarchical Autoregressive Transformer (HAR). All models maintain strictly aligned tokenization rates between audio tokens*

**分词器设计消融**（Appendix Table 6）：
- **组合式分区域 SVQ 分词器 vs 全身单一分词器**：FGD 4.57 vs 6.84，BC 0.794 vs 0.753，Div 13.91 vs 11.23。区域专门化的分词器能更精准地捕获各身体部位的运动模式，避免全局码本中的量化碰撞。

**码本大小**（Appendix Table 3）：K=2048 获得最佳质量；K=512 时 FGD 升至 6.63、BC 降至 0.734，表明过小码本导致严重的量化碰撞和表达力不足。

**分类器自由引导（CFG）尺度**（Appendix Table 5）：γ=1.25 时性能最优；γ 过大（如 2.0）使 FGD 急剧上升至 6.42，多样性下降，表明过度引导会牺牲动作的自然多样性。

**掩码调度策略**（Table 2f）：固定余弦退火调度优于均匀随机掩码，BC 0.794 vs 0.776，证明在训练后期逐步降低掩码率有助于模型平稳过渡到自回归推理。

### 失败模式与局限性

尽管 LiveGesture 在流式约束下取得了优异性能，分析揭示了以下局限：

1. **FGD 差距**：由于无法访问未来帧，LiveGesture 在 FGD 上始终略逊于离线最优模型。这在长时域连贯动作（如持续的手势保持）中尤为明显，因为离线方法可以利用双向上下文进行时序精修。

2. **面部逼真度不足**：面部 MSE 为 1.241，弱于 GestureLSM 的 1.021。面部运动的细粒度细节（如微表情、唇形同步）在因果约束下更难建模，可能影响虚拟人的整体自然度。

3. **数据集泛化风险**：当前评估仅限于 BEAT2 数据集，对新说话人、新场景（如独白、不同语言）的泛化能力尚未验证。模型在域外数据上的节拍一致性和多样性可能显著下降。

4. **上游错误传播**：模型依赖并行流式语音系统（如 VITA-Audio），语音识别/合成的错误可能直接传播至手势生成，导致不协调的动作。

5. **首帧延迟**：250 ms 的首帧延迟在对话场景中可接受，但在超低延迟交互（如 VR 遥现）中仍有优化空间。

6. **极长时域稳定性**：在几分钟到几十分钟的连续生成中，如何保证动作的长期连贯性并避免模式坍塌，是当前未充分验证的开放问题。

### 补充图表

![[assets/figures/papers/paper_list_l993_https_arxiv_org_abs_2604_10927/figures/006_Figure_5.jpg]]
*Figure 5: Interactive human–avatar conversation enabled by LiveGesture. User speech is converted into a spoken reply by VITA-Audio, while our LiveGesture streaming gesture model simultaneously generates synchronized full-body SMPL-X motions from live audio, allowing the avatar to respond in real time*

![[assets/figures/papers/paper_list_l993_https_arxiv_org_abs_2604_10927/figures/016_Table_6.jpg]]
*Table 6: Comparison between a single full-body SVQ tokenizer and compositional per-region SVQ tokenizers. Both variants use the same total codebook capacity (2048 entries with 128-d embeddings)*

![[assets/figures/papers/paper_list_l993_https_arxiv_org_abs_2604_10927/figures/013_Table_3.jpg]]
*Table 3: Effect of codebook size in the SVQ motion tokenizer on full-body gesture generation. Larger codebooks increase representational capacity and yield consistent gains across all metrics*

![[assets/figures/papers/paper_list_l993_https_arxiv_org_abs_2604_10927/figures/015_Table_5.jpg]]
*Table 5: Effect of classifier-free guidance scale γ on streaming gesture generation*

## 方法谱系与知识库定位

### 1. 任务定位与核心瓶颈

LiveGesture 解决的是**实时流式协语音全身手势生成**问题：给定连续到达的音频块，模型需在严格零前瞻（zero look-ahead）约束下，以低延迟在线输出与语音节拍同步的 SMPL-X 全身姿态序列。

现有协语音手势生成方法在方法谱系上可分为三类，但均无法满足流式交互需求：

- **离线自回归/Transformer 方法**：如 **CaMN**、**TalkShow**、**MambaTalk**、**SynTalker**、**RAG-Gesture** 等，依赖完整语音输入进行双向时序建模，生成质量高但延迟不可控，无法流式部署。
- **离线扩散/概率方法**：如 **DiffSHEG**、**DisCo**、**ProbTalk**、**EMAGE**，通过扩散过程或概率图模型建模动作分布，虽能产生多样化手势，但推理需多步去噪或全局优化，天然不支持因果流式生成。
- **分层/混合架构**：如 **HA2G** 和 **GestureLSM**（离线最佳），GestureLSM 在 BEAT2 上取得 FGD=4.25 的最优质量，但其设计依赖完整话语的双向编码，无法在零前瞻下运行。

**核心瓶颈**在于：将全身运动分解为独立区域建模会丢失区域间协调，而全局联合建模又引入非因果依赖，导致现有方法在“低延迟”与“高动作质量”之间形成根本性 trade-off。LiveGesture 的分层因果自回归架构正是针对这一瓶颈的系统性解决方案。

### 2. 方法谱系中的创新定位

LiveGesture 在方法谱系中的独特位置体现在三个层面的因果化改造：

**（1）运动分词器的因果化**：传统 VQ-VAE 分词器（如 **EMAGE** 所用）采用双向编码器-解码器，解码时需访问未来帧。LiveGesture 的 SVQ 分词器采用非对称架构——双向编码器捕获全局上下文，但解码器严格因果，配合区域特定码本，首次在离散词元空间中实现零前瞻解码。这一设计使运动词元天然适配流式自回归生成，而非事后适配。

**（2）全身协调的因果分层建模**：区别于 **CaMN** 的全局纠缠或 **TalkShow** 的独立区域建模，LiveGesture 采用“区域专家 + 因果时空融合”的两级架构。区域专家（xAR）各自以因果 Transformer 学习局部动态，冻结后通过因果交叉注意力在 xAR-Fuse 中捕获全身协调。这本质上是将“局部自回归”与“全局因果融合”解耦，使模型在严格因果约束下仍能建模区域间依赖。

**（3）流式误差的主动缓解**：标准教师强制（teacher forcing）训练在流式推理时面临误差累积问题。LiveGesture 引入不确定性引导的混合掩码训练（UGM），在融合阶段以自适应概率掩码运动词元，迫使模型学习从部分观测中恢复全身动作。这一策略与分类器自由引导（CFG）配合，在不违反因果约束的前提下有效缓解了流式漂移。

### 3. 适用边界与局限

**适用场景**：LiveGesture 专为实时人机对话场景设计，如虚拟人直播、交互式数字人助手、VR 遥现中的全身化身驱动。其 250 ms 首帧延迟和 <50 ms 的逐块推理延迟（每 200 ms 音频块）使其可部署于近实时交互系统。

**已知局限**：

| 局限维度 | 具体表现 | 证据 |
|---------|---------|------|
| **时序精度上限** | FGD=4.57，弱于离线最佳 GestureLSM 的 4.25，因无法利用未来帧进行时序精修 | Table 1 |
| **面部运动逼真度** | 面部 MSE=1.241，弱于 GestureLSM 的 1.021，面部模块的流式生成质量仍有差距 | Table 1 |
| **数据泛化性** | 仅在 BEAT2 数据集上验证，对新说话人、新语言、独白等场景的泛化能力未评估 | 实验设置 |
| **上游依赖风险** | 依赖并行流式语音系统（如 VITA-Audio），语音识别/合成的错误可能传播至手势生成 | Figure 5 应用演示 |
| **超长时域稳定性** | 未验证在数十分钟连续生成中的动作连贯性与多样性保持能力 | 未涉及 |

### 4. 开放问题与后续方向

基于 LiveGesture 的架构特点和当前局限，以下开放问题值得关注：

1. **FGD 差距的因果闭合**：能否通过结构约束（如引入可学习的因果先验）或知识蒸馏（从离线教师模型迁移时序知识至因果学生模型），在不访问未来帧的前提下进一步缩小与离线方法的 FGD 差距？

2. **语义手势的流式增强**：当前模型主要依赖音频韵律驱动节拍手势，文本语义的融入方式较为简单（可选文本词元拼接）。如何更有效地将实时流式文本语义（如指代、隐喻、空间描述）注入因果生成过程，以增强语义手势的表达力？

3. **跨任务因果架构迁移**：SVQ 分词器 + 分层因果自回归的架构设计，能否推广到其他连续运动生成任务（如舞蹈、手语、体育动作），这些任务同样面临实时性与协调性的双重约束？

4. **自适应掩码策略**：不确定性引导的掩码调度（UGM）当前采用固定余弦退火，是否可以设计自适应学习机制，根据生成状态动态调整掩码概率，进一步提升流式鲁棒性？

5. **极低延迟优化**：当前 250 ms 首帧延迟和 0.5M 参数的音频编码器在超低延迟场景（如 VR 遥现要求 <100 ms 端到端延迟）仍有压缩空间，轻量化因果音频编码器和更激进的下采样策略值得探索。

6. **长时域连贯性保证**：在数十分钟甚至小时级的连续流式生成中，如何保证动作的长期多样性不退化、避免重复模式，是实际部署必须面对的问题。

## 原文 PDF

![[paperPDFs/CVPR_2026/LiveGesture_Streamable_Co_Speech_Gesture_Generation_Model.pdf]]

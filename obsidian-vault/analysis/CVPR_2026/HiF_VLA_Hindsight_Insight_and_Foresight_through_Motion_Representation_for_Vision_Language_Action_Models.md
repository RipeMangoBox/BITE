---
title: "HiF-VLA: Hindsight, Insight and Foresight through Motion Representation for Vision-Language-Action Models"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/HiF_VLA_Hindsight_Insight_and_Foresight_through_Motion_Representation_for_Vision_Language_Action_Models.pdf
project_link: "https://hifvla.github.io"
code_link: "https://github.com/OpenHelix-Team/HiF-VLA"
aliases:
- HV
- HiF-VLA
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/representation_self_supervised_transfer
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 使用运动向量作为时空压缩表征，将过去动态编码为后见先验，预测未来运动作为预见，并通过后见调制的联合专家模块在统一潜空间中融合时序信息以生成时序一致的动作。
primary_logic: 运动向量能够紧凑且忠实地捕获状态间的任务相关动态变化，同时滤除静态像素噪声；通过双向时序推理（后见与预见），可使VLA在‘边思考边行动’的范式下实现长程操作。
claims:
- HiF-VLA 在 LIBERO-Long 和 CALVIN ABC-D 上显著超越现有方法，并保持极低的额外推理延迟。
- 运动表征替代堆叠帧显著降低 GPU 内存和推理延迟，同时提升成功率。
- 后见调制联合专家优于直接向 VLM 注入后见，验证了条件化嵌入的有效性。
- 双向联合专家比因果分离提升 7% 成功率，证明动作与运动交互建模的必要性。
---

# HiF-VLA: Hindsight, Insight and Foresight through Motion Representation for Vision-Language-Action Models

> [!tip] 核心洞察
> 运动向量能够紧凑且忠实地捕获状态间的任务相关动态变化，同时滤除静态像素噪声；通过双向时序推理（后见与预见），可使VLA在‘边思考边行动’的范式下实现长程操作。

| 字段 | 内容 |
|------|------|
| 中文题名 | HiF-VLA：基于运动表征的视觉-语言-动作模型中的回顾、洞察与前瞻 |
| 英文题名 | HiF-VLA: Hindsight, Insight and Foresight through Motion Representation for Vision-Language-Action Models |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2512.09928) · [Project](https://hifvla.github.io) · [Code](https://github.com/OpenHelix-Team/HiF-VLA) |
| Topic | #topic/vision_multimodal_applications #topic/representation_self_supervised_transfer #topic/vision_multimodal_applications/image_and_video_generation |
| Method | HiF-VLA |
| Dataset | LIBERO-Long, CALVIN ABC-D, LIBERO 四套件平均 |

> [!tip] 效果简介
> - LIBERO-Long (multi-view) 上，平均成功率 SR (%) 96.4 vs 94.0 (OpenVLA-OFT) (+2.4)。
> - CALVIN ABC-D (multi-view) 上，平均连续完成指令数 Avg.Len. 4.35 vs 4.10 (OpenVLA-OFT) (+0.25)。
> - LIBERO 四套件平均 上，平均成功率 SR (%) 98.0 vs 97.1 (OpenVLA-OFT) (+0.9)。

## 概要

视觉-语言-动作（VLA）模型在机器人操控中展现出强大的泛化能力，但其时序建模存在根本性瓶颈：现有方法普遍基于马尔可夫假设，仅依赖当前观测 $o_t$ 预测动作，导致长期任务中动作连贯性差、时序近视严重。部分工作通过堆叠历史帧引入时序信息，却带来大量像素冗余与计算开销，分散模型对任务相关动态的注意力；而生成像素级子目标的方法则推理成本高昂且结构弱。**HiF-VLA**（CVPR 2026）针对上述问题，提出以**运动向量**作为时空压缩表征，实现双向时序推理——编码过去动态为后见先验，预测未来运动为预见，并通过后见调制的联合专家模块在统一潜空间中融合时序信息，使 VLA 在“边思考边行动”的范式下生成时序一致的动作。

核心结论如下：

- **运动表征替代堆叠帧**：HiF-VLA 使用运动向量捕获帧间任务相关动态，滤除静态像素噪声，在 LIBERO-Long 上以 96.4% 的平均成功率超越 OpenVLA-OFT（94.0%），同时将推理延迟降至 121.6 ms，相比堆叠 8 帧历史的方法减少高达 78% 的延迟开销。
- **双向时序推理有效**：后见先验与预见推理的联合建模使模型在 CALVIN ABC-D 上平均连续完成指令数达到 4.35，优于基线 4.10；消融实验表明，双向联合专家比因果分离设计提升 7% 成功率，验证了动作与运动交互建模的必要性。
- **后见调制优于直接注入**：将后见信息作为条件化嵌入送入联合专家解码器，而非直接注入 VLM，在 LIBERO-Long 上取得更高成功率，表明条件化调制对时序融合更为有效。
- **“边思考边行动”协同收敛**：联合预测未来运动与动作可加速运动损失收敛，验证了双流协同训练的正向反馈。

HiF-VLA 将 VLA 的时序感受野从单向扩展为双向，以紧凑、结构化的运动表征实现了高效的长程操作推理，在多个基准上达到最优性能，同时保持极低的额外推理开销。

### 具身操作中的时序近视困境

视觉-语言-动作模型将大规模预训练的视觉-语言模型适配为机器人动作预测器，已在多种操作任务上展现出强大的泛化能力。然而，现有 VLA 模型普遍遵循马尔可夫假设——仅依赖当前观测 $o_t$ 和任务指令 $l$ 来预测动作序列：

$$\tilde a_{t:t+n} \sim P_\theta(a_{t:t+n} \mid o_t, l)$$

这一简化范式在长程操作中暴露出根本性缺陷：模型缺乏对过去执行状态的有效记忆，无法感知任务进展与历史动态，导致动作序列随时间推移逐渐偏离任务目标，出现动作连贯性差、子任务间衔接断裂等问题。我们将这一现象称为 VLA 模型的**时序近视**。

### 现有时序建模方案的局限

为缓解时序近视，研究者尝试了多种策略，但均存在显著局限：

**堆叠历史帧**：将多帧原始 RGB 图像沿通道或时间维度拼接后输入模型，虽能提供时序信息，但引入了大量像素冗余——静态背景、无关物体等噪声被反复编码，不仅推高 GPU 显存和推理延迟，更分散了模型对任务相关动态变化的注意力。

**像素级子目标生成**：通过预测未来图像作为中间表示来引导动作规划，但图像生成本身计算代价高昂，且生成的子目标缺乏结构化约束，难以精确指导底层动作执行。

上述方案的核心症结在于：它们试图用**密集的像素空间**承载时序信息，却未提炼出真正决定任务进展的**动态变化**。

### 运动表征的潜力与双向时序推理

本文的出发点是：在操作任务中，真正影响决策的不是每一帧的全部像素，而是帧与帧之间**发生了什么变化**——物体的位移、机械臂的轨迹、交互引起的视觉后果。这些变化可以紧凑地编码为**运动向量**：

$$\text{MV}_{t-1:t}(x,y) = (x_t - x_{t-1}, y_t - y_{t-1})$$

运动向量天然滤除了静态像素噪声，仅保留任务相关的动态信号，且维度远低于原始图像。更重要的是，运动表征天然支持**双向时序推理**：回顾历史运动可以理解“已经做了什么”，预测未来运动可以推断“接下来会发生什么”，二者结合可实现“边思考边行动”的长程操作范式。

### HiF-VLA 的设计动机

基于上述洞察，HiF-VLA 以运动向量为统一时序表征，构建三阶段流水线：
1. **后见先验获取**：从历史帧序列中提取运动向量，编码为结构化的后见令牌 $M_h$，以极低计算代价捕获过去动态；
2. **预见推理与洞察**：在 VLM 中利用任务指令和当前观测，同时预测未来运动令牌 $M_f$ 和动作潜在令牌 $A_f$；
3. **后见调制联合专家**：通过 AdaLN 条件化和交叉流双向注意力，在统一潜空间中融合后见、预见和动作表征，生成时序一致的动作预测。

这一设计使 HiF-VLA 在保持极低额外推理延迟的前提下，显著扩展了 VLA 的时序感受野，为长程操作任务提供了结构化、高效率的时序推理能力。

## 核心方法与创新机理

### 1. 问题诊断：时序近视的瓶颈

现有视觉-语言-动作（VLA）模型普遍受限于**马尔可夫假设**，仅依据当前观测 $o_t$ 预测动作序列 $a_{t:t+n}$，导致在长程任务中动作连贯性差、时序一致性不足。部分工作尝试通过堆叠多帧历史图像来扩展时序感受野，但这一策略引入大量像素冗余，不仅使GPU显存和推理延迟急剧上升（**Figure 3b** 显示，历史长度增至8时，多帧基线推理延迟超过原始VLA的4.5倍），还分散了模型对任务相关动态的注意力。另一类方法生成像素级子目标作为中间表示，但同样面临计算开销大、时序结构弱的问题。

**核心瓶颈**：如何在保持计算效率的前提下，为VLA注入紧凑且任务相关的时序信息，使其具备长程操作能力。

### 2. 解决方案：运动表征驱动的双向时序推理

HiF-VLA 的核心创新在于**用运动向量（Motion Vector, MV）作为时空压缩表征**，替代冗余的像素堆叠，实现双向时序推理。具体而言，方法引入三个关键设计：

- **后见先验（Hindsight Prior）**：从历史帧序列中提取运动向量 $m_{t-h:t}$，编码为紧凑的后见令牌 $M_h$，捕获过去动态而不携带静态像素噪声。运动向量定义为相邻帧间宏块的位置偏移 $MV_{t-1:t}(x,y) = (x_t - x_{t-1}, y_t - y_{t-1})$，是压缩历史动态的基本单元。

- **预见推理（Foresight Reasoning）**：在VLM中引入可学习的预见查询令牌，与任务指令和当前观测共同推理，同时预测未来运动 $m_{t:t+n}$ 和动作潜在令牌 $A_f$，形成“边思考边行动”的双流协同范式。

- **后见调制联合专家（Hindsight-Modulated Joint Expert）**：采用交叉流双向注意力与自适应层归一化（AdaLN）条件化机制，将后见 $M_h$、预见 $M_f$ 和动作 $A_f$ 令牌在统一潜空间中融合。AdaLN 利用后见调节向量 $h_c$ 对表示 $z$ 进行缩放和平移：$\mathrm{AdaLN}(z; h_c) = \gamma(h_c) \cdot \frac{z - \mu(z)}{\sigma(z)} + \beta(h_c)$，实现条件化调制。

整体推理过程可形式化为：
$$(\widetilde a_{t:t+n}, \widetilde m_{t:t+n}) \sim P_{\theta}^{\prime} (a_{t:t+n}, m_{t:t+n} | o_t, l, m_{t-h:t}^{\mathrm{his}})$$

### 3. 相对于基线的关键变化

相对于 **OpenVLA-OFT**（使用L1回归的VLA模型，无显式时序建模），HiF-VLA 在四个关键维度上进行了系统性改进：

| 改进维度 | 基线方法 | HiF-VLA | 证据锚点 |
|---------|---------|---------|---------|
| **时序输入** | 仅当前观测 $o_t$ | 历史运动向量 $m_{t-h:t}$ 经后见编码器产生后见令牌 $M_h$，作为条件先验 | Sec. 3.2 |
| **未来预测** | 无未来预测，仅输出动作 | VLM中引入可学习预见查询令牌，同时预测未来运动 $m_{t:t+n}$ 和动作潜在令牌 $A_f$ | Sec. 3.3 |
| **融合机制** | 直接使用VLM输出通过动作头回归动作 | 后见调制联合专家模块，采用交叉流双向注意力与AdaLN条件化 | Sec. 3.4 |
| **动作预测范式** | 仅动作回归 | 联合预测未来运动与动作，形成“边思考边行动”的双流协同 | Sec. 3.1, Eq(2) |

### 4. 创新点的实证支撑

消融实验系统性地验证了每个创新设计的有效性：

- **运动表征优于本体状态**：运动向量（MV）替代机器人本体状态信息（S）后，成功率从92.0%提升至94.4%，表明MV能够捕获物体交互等视觉动态，而本体状态无法充分反映环境变化（**Table 6a**）。

- **双向联合专家优于因果分离**：双向联合专家（Bi-[M\|A]）相比因果分离设计（Causal-[M\|A]）提升7%成功率（94.4% vs 87.4%），验证了动作与运动交互建模的必要性（**Table 6b**）。

- **后见条件化嵌入优于直接注入**：将后见信息作为联合专家的条件化嵌入，相比直接注入VLM取得更高成功率，验证了条件化调制机制的有效性（**Figure 4**, Sec. 4.4）。

- **联合预见与动作训练产生协同效应**：完整的双流训练比仅训练运动预测分支收敛更快，验证了“边思考边行动”范式的协同效果（**Figure 7**, Sec. 8.4）。

- **效率优势**：运动表征替代堆叠帧后，HiF-VLA在保持低推理延迟的同时取得更高成功率——在历史长度8的设置下，推理延迟仅从121.6ms微增至约130ms，而多帧基线已超过4.5倍原始延迟（**Table 3**, **Figure 3b**）。

### 5. 方法局限与开放问题

尽管HiF-VLA在长程任务上取得显著提升，仍存在以下局限：

- **3D感知依赖**：真实场景中因空间几何判断和深度估计误差导致的失败（如提前松爪、按压不足）表明，当前方法对精确3D感知的依赖较强，未来可集成更丰富的3D表示（如点云、深度图）。

- **预见长度限制**：增加预见长度（如 $n=16$）会降低性能，单次预测的时间跨度受误差累积限制。

- **运动提取的通用性**：运动向量的提取依赖于视频编码标准（MPEG-4），对训练数据的帧率与格式可能有特定要求，在更广泛场景下的通用性有待验证。

**开放问题**：如何将运动表征扩展到更高级的推理任务（如安全性预测、物理规律学习），以及在大规模多任务数据上保证联合预见与动作的训练稳定性，是值得进一步探索的方向。

HiF-VLA 的核心洞察在于：**运动向量（Motion Vector, MV）** 能够紧凑且忠实地捕获状态间的任务相关动态变化，同时滤除静态像素噪声。基于此，HiF-VLA 构建了一个双向时序推理框架，将过去动态编码为“后见先验”，将未来运动预测为“预见”，并通过一个统一潜空间中的融合模块生成时序一致的动作序列。整体推理范式可形式化为：

$$(\widetilde a_{t:t+n}, \widetilde m_{t:t+n}) \sim P_{\theta}^{\prime} (a_{t:t+n}, m_{t:t+n} | o_t, l, m_{t-h:t}^{\mathrm{his}})$$

给定当前观测 $o_t$、任务指令 $l$ 和历史运动向量 $m_{t-h:t}^{\mathrm{his}}$，HiF-VLA 联合预测未来动作块 $\widetilde a_{t:t+n}$ 与未来运动向量 $\widetilde m_{t:t+n}$，形成“边思考边行动”（think-while-acting）的双流协同范式。

### 流水线总览

HiF-VLA 由三个核心模块串联构成，其数据流与模块关系如 **Figure 2** 所示：

![[assets/figures/papers/paper_list_l961_https_arxiv_org_abs_2512_09928/figures/002_Figure_2.jpg]]
*Figure 2: HiF-VLA Pipeline. (a) In Hindsight Prior Acquisition (see Sec. 3.2), HiF-VLA encodes dense historical frame sequences into compact Motion Vector (MV) streams, forming structured hindsight primitives that capture temporal dynamics without pixel redundancy. (b) In Foresight Reasoning with Insight (see Sec. 3.3), the VLM interprets the task instruction and current observation to infer plausible foresight motions and corresponding latent action tokens. (c) Finally, the Hindsight-Modulated Joint Expert (see Sec. 3.4) fuses hindsight, foresight, and action representations within a unified latent space, producing temporally consistent and causally coherent action predictions*

1. **后见先验获取（Hindsight Prior Acquisition）**：从密集历史帧序列中提取运动向量流，编码为结构化的后见令牌 $M_h$，捕获过去时序动态而不引入像素冗余。

2. **预见推理与洞察（Foresight Reasoning with Insight）**：在 VLM 中，基于任务指令和当前观测，利用可学习的预见查询令牌生成预见运动令牌 $M_f$ 和动作潜在令牌 $A_f$，实现对未来的结构化推理。

3. **后见调制联合专家（Hindsight-Modulated Joint Expert）**：采用交叉流双向注意力与 AdaLN 条件化机制，将后见令牌 $M_h$、预见令牌 $M_f$ 和动作令牌 $A_f$ 在统一潜空间中融合，产生时序一致且因果连贯的动作预测。

最后，融合后的表示分别经**动作头（Action Head）**和**运动头（Motion Head）**解码为未来动作块与预测运动向量。

### 与现有方法的本质差异

现有 VLA 方法或仅依赖瞬时观测（如 **OpenVLA** 系列），或通过堆叠原始图像帧引入历史信息，但后者带来大量像素冗余和计算开销，且分散模型对任务相关动态的注意力。HiF-VLA 以运动向量替代堆叠帧作为时空压缩表征，将时序建模从像素空间提升到运动语义空间，实现了三个关键转变：

| 设计维度 | 基线方法（OpenVLA-OFT） | HiF-VLA |
|---------|----------------------|---------|
| 时序输入 | 仅当前观测 $o_t$ | 历史运动向量 $m_{t-h:t}$ 经后见编码器产生条件先验 |
| 未来预测 | 无，仅输出动作 | VLM 中引入预见查询令牌，同时预测未来运动 $m_{t:t+n}$ 和动作潜在令牌 $A_f$ |
| 融合机制 | 直接使用 VLM 输出通过动作头回归 | 后见调制联合专家，采用交叉流双向注意力与 AdaLN 条件化 |
| 预测范式 | 仅动作回归 | 联合预测未来运动与动作，形成双流协同 |

### 联合专家融合机制

后见调制联合专家（**Figure 6**）是整个框架的关键设计。它并非简单地将后见信息注入 VLM，而是作为独立的专家解码器，通过自适应层归一化（AdaLN）接收后见调节向量 $h_c$ 进行条件化调制：

$$\mathrm{AdaLN}(z; h_c) = \gamma(h_c) \cdot \frac{z - \mu(z)}{\sigma(z)} + \beta(h_c)$$

该模块内部采用**交叉流双向注意力**，允许预见运动令牌与动作潜在令牌之间进行充分的交互建模。消融实验表明，双向联合专家比因果分离设计提升 **7%** 成功率（94.4% vs 87.4%），验证了动作与运动交互建模的必要性。

### 训练目标

总损失为动作 L1 损失与运动 L1 损失的加权和：

$$\mathcal{L}_{\mathrm{all}} = \mathcal{L}_{A} + \lambda \cdot \mathcal{L}_{MV}$$

其中 $\lambda=0.01$ 平衡动作精度与运动重建质量。联合训练中，动作预测分支的存在可加速运动损失的收敛，验证了“边思考边行动”范式的协同效果。

HiF-VLA 的核心创新在于将运动向量（Motion Vector, MV）作为时空压缩表征，替代传统 VLA 模型中的原始图像堆叠，实现双向时序推理。其流水线由三个关键模块构成：**后见先验获取**、**预见推理与洞察**、**后见调制联合专家**。

### 3.1 问题形式化与核心公式

传统 VLA 模型基于马尔可夫假设，仅依赖当前观测 $o_t$ 和语言指令 $l$ 预测未来动作块：

$$ \tilde{a}_{t:t+n} \sim P_{\theta}(a_{t:t+n} \mid o_t, l) \tag{1} $$

HiF-VLA 将历史运动向量 $m_{t-h:t}^{\mathrm{his}}$ 作为条件先验引入，并联合预测未来动作块与未来运动向量，形成“边思考边行动”的双流范式：

$$ (\tilde{a}_{t:t+n}, \tilde{m}_{t:t+n}) \sim P_{\theta}^{\prime}(a_{t:t+n}, m_{t:t+n} \mid o_t, l, m_{t-h:t}^{\mathrm{his}}) \tag{2} $$

其中 $m_{t-h:t}^{\mathrm{his}}$ 是过去 $h$ 步的运动向量序列，$\tilde{m}_{t:t+n}$ 是预测的未来 $n$ 步运动向量。运动向量的加入使模型能够显式建模时序动态，同时避免原始像素的冗余。

### 3.2 后见先验获取

该模块的核心是将密集的历史帧序列压缩为结构化的运动向量流。运动向量定义为相邻帧间宏块的位置偏移：

$$ \mathrm{MV}_{t-1:t}(x,y) = (x_t - x_{t-1}, y_t - y_{t-1}) \tag{3} $$

运动向量通过 MPEG-4 视频编码标准从历史帧序列中提取，能够紧凑地捕获场景中的任务相关动态变化（如物体移动、机械臂运动），同时滤除静态背景的像素噪声。提取后的运动向量流经后见编码器处理，生成后见令牌 $M_h$，作为后续融合的条件先验。

**关键设计动机**：运动向量具有三个优势——（1）低维度，相比堆叠 RGB 帧大幅减少计算开销；（2）动态聚焦，天然过滤静态冗余，保留任务相关的运动信息；（3）结构化，相邻帧间的偏移量直接编码了时序因果关系。

### 3.3 预见推理与洞察

在 VLM 内部，HiF-VLA 引入可学习的预见查询令牌（$K_f$ 个）和空动作令牌（$K_a$ 个），与任务指令和当前观测的嵌入一同输入 VLM。VLM 采用非因果注意力掩码，使令牌间可双向交互，并行推理未来运动与动作：

$$ (M_f, A_f) = F_{\theta}(o_t, l) \tag{4} $$

其中 $M_f$ 为预见运动令牌，$A_f$ 为动作潜在令牌。与生成像素级子目标的方案不同，HiF-VLA 预测结构化的运动向量作为未来时空目标，这既降低了预测难度，又与动作执行直接对齐。

### 3.4 后见调制联合专家

该模块是 HiF-VLA 融合时序信息的关键。后见令牌 $M_h$ 经处理后生成条件调节向量 $h_c$，通过自适应层归一化（AdaLN）对联合专家进行调制：

$$ \mathrm{AdaLN}(z; h_c) = \gamma(h_c) \cdot \frac{z - \mu(z)}{\sigma(z)} + \beta(h_c) \tag{5} $$

其中 $\gamma(h_c)$ 和 $\beta(h_c)$ 是由 $h_c$ 生成的缩放和平移参数。联合专家内部采用交叉流双向注意力机制，融合后见令牌 $M_h$、预见运动令牌 $M_f$ 和动作潜在令牌 $A_f$：

$$ \tilde{M}_f, \tilde{A}_f = \mathrm{JointExpert}(M_f, A_f \mid h_c) \tag{6} $$

**消融验证**：实验表明，双向联合专家（Bi-[M|A]）比因果分离设计（Causal-[M|A]）提升 7% 成功率（94.4% vs 87.4%），验证了动作与运动交互建模的必要性。同时，将后见作为专家条件化嵌入优于直接注入 VLM，说明 AdaLN 调制机制对时序信息的有效利用至关重要。

### 3.5 训练目标

融合后的令牌分别通过动作头和运动头解码为最终预测。训练损失由两部分组成：

$$ \mathcal{L}_{\mathrm{all}} = \mathcal{L}_{A} + \lambda \cdot \mathcal{L}_{MV} \tag{7} $$

其中 $\mathcal{L}_{A} = \frac{1}{n}\sum_{j=1}^{n}|a_{t+j} - \tilde{a}_{t+j}|$ 为动作 L1 损失，$\mathcal{L}_{MV} = \frac{1}{n}\sum_{j=1}^{n}|m_{t+j} - \tilde{m}_{t+j}|$ 为运动 L1 损失。$\lambda=0.01$ 平衡动作精度与运动重建质量。消融实验表明，联合预见与动作训练可加速运动损失收敛，验证了双流协同的有效性。

![[assets/figures/papers/paper_list_l961_https_arxiv_org_abs_2512_09928/figures/009_Figure_6.jpg]]
*Figure 6: Architecture of the hindsight-modulated joint expert*

![[assets/figures/papers/paper_list_l961_https_arxiv_org_abs_2512_09928/figures/006_Figure_4.jpg]]
*Figure 4: Performance comparison on different hindsight embedding locations. (a) represents direct injection into the VLM, and (b) represents conditional embedding as an expert decoder. (c) shows the performance of both on LIBERO-Long*

## 实验与关键发现

### 4.1 实验设置与基准

HiF‑VLA 在两个主流长程机器人操作基准上进行评估：**LIBERO‑Long**（10 个长程任务，涵盖第三视角与多视角输入）和 **CALVIN ABC‑D**（多阶段连续指令执行）。主基线为 **OpenVLA‑OFT**（无显式时序建模的 VLA 模型，使用 L1 回归），同时对比了一系列现有方法，包括基于堆叠帧的时序增强方案和像素级子目标生成方法。所有方法使用相同的数据划分与评估协议，带 ∗ 的结果均使用官方开源代码复现，比较在相同的摄像头配置下进行，公平性较高。

### 4.2 主实验结果

**LIBERO‑Long 基准。** 如 Table 1 所示，HiF‑VLA 在第三视角设置下取得 94.4% 的平均成功率（Avg. SR），在多视角设置下进一步提升至 96.4%，分别超出 OpenVLA‑OFT 基线 2.4 和 2.3 个百分点。这一结果验证了双向时序推理（后见与预见）在长程任务中的有效性——单纯依赖当前观测的 VLA 模型因马尔可夫假设而患有时序近视，而 HiF‑VLA 通过运动向量捕获历史动态并预测未来运动，显著增强了动作的时序一致性。

**CALVIN ABC‑D 基准。** 如 Table 2 所示，HiF‑VLA 在 CALVIN ABC→D 多视角设置下取得 4.35 的平均连续完成指令数（Avg. Len.），超出 OpenVLA‑OFT 基线 0.25，在第三视角设置下同样保持领先（4.08 vs. 3.82）。CALVIN 的连续指令执行要求模型在未见过的任务组合中保持稳定的时序推理能力，HiF‑VLA 的增益表明运动表征在多阶段任务迁移中的泛化优势。

**LIBERO 四套件全面比较。** 在 LIBERO 的 Spatial、Object、Goal 和 Long 四个套件上，HiF‑VLA 平均成功率 98.0%，超过 OpenVLA‑OFT 的 97.1%（Table 4），进一步证明了该方法在不同任务类型上的鲁棒性。

### 4.3 效率与冗余分析

现有堆叠帧方法虽能提供时序信息，但引入大量像素冗余和计算开销。Table 3 对比了多帧基线变体与 HiF‑VLA 变体在历史长度固定为 4 时的效率：HiF‑VLA 的完整版本（+ Hindsight + Foresight）仅需 32.2 GB 峰值 GPU 内存和 121.6 ms 推理延迟，而多帧基线在相同历史长度下内存与延迟均显著更高。Figure 3b 进一步显示，多帧基线的推理延迟随历史长度几乎线性增长，在历史长度 8 时超过原始 VLA 的 4.5 倍；相比之下，HiF‑VLA 的延迟增长极为平缓，保持了接近常数的计算开销。这一效率优势源于运动向量作为时空压缩表征的本质：它仅保留帧间的宏块位移信息，滤除了静态像素噪声。

### 4.4 消融研究

**运动表征 vs. 本体状态。** Table 6(a) 显示，使用运动向量（MV）作为历史输入的变体取得 94.4% 成功率，显著优于使用机器人本体状态信息（S）的 92.0%。这表明运动向量能够捕获物体交互、遮挡变化等视觉动态，而这些信息无法从关节角度等本体状态中直接获取。

**双向联合专家 vs. 因果分离。** Table 6(b) 对比了双向联合专家（Bi‑[M|A]）与因果分离设计（Causal‑[M|A]）。双向联合专家允许动作令牌与运动令牌之间的交叉流注意力交互，取得 94.4% 成功率，而因果分离变体仅为 87.4%，差距达 7 个百分点。这一结果强有力地验证了动作与运动交互建模的必要性——“边思考边行动”范式要求动作预测与运动推理在统一潜空间中协同，而非独立进行。

**后见条件化嵌入位置。** Figure 4 对比了两种后见信息注入方式：直接注入 VLM（VLM‑based embedding）与作为专家解码器的条件化嵌入（expert‑conditioned embedding）。后者在 LIBERO‑Long 上取得更高成功率，验证了后见调制联合专家模块的设计优势——通过 AdaLN 条件化（Eq(5)）对预见和动作令牌进行缩放和平移调制，比简单地将后见令牌拼接入 VLM 输入序列更有效地利用了历史动态信息。

**超参数敏感性。** Table 5 报告了关键超参数的消融结果：(1) 后见长度 8 时性能最优（SR 96.4%），过长或过短均导致性能下降；(2) 预见损失权重 λ=0.01 时取得最佳平衡，过大权重会干扰动作预测精度；(3) 联合专家深度 6 为最优配置。Figure 3c 进一步展示了后见长度在不同视角下对成功率的影响曲线。

**联合预见与动作训练的协同效应。** Figure 7 展示了训练过程中预见运动 L1 损失的收敛曲线。完整 HiF‑VLA 架构（w/ action prediction）的损失下降速度明显快于仅保留运动预测分支的变体（w/o action prediction），表明联合动作预测为运动推理提供了有效的学习信号，二者在训练中形成正向协同。

### 4.5 失败模式分析

尽管 HiF‑VLA 在基准测试中表现优异，真实世界实验中仍暴露出若干典型失败模式（Figure 10）：(1) **空间几何判断误差**——在“将方块放入盘子”任务中，机械臂因深度估计偏差而提前松爪，导致物体掉落；(2) **按压不足**——在“按顺序按下按钮”任务中，末端执行器未施加足够压力即判定任务完成；(3) **预见误差累积**——增加预见长度（如 n=16）会导致预测的运动向量偏离真实轨迹，降低长程动作的可靠性。这些失败案例表明，当前方法对精确 3D 感知的依赖仍是瓶颈，运动向量虽能压缩时序动态，但无法替代深度信息，未来可集成更丰富的 3D 表示（如点云、深度图）以提升空间操作精度。

![[assets/figures/papers/paper_list_l961_https_arxiv_org_abs_2512_09928/figures/003_Table_1.jpg]]
*Table 1: Performance comparison on the LIBERO-Long benchmark. We report the average success rate (%) across 10 tasks with “Avg. SR”. Results marked with “∗” were reproduced using the official open-source code. Bold indicates the best performance*

![[assets/figures/papers/paper_list_l961_https_arxiv_org_abs_2512_09928/figures/004_Table_2.jpg]]
*Table 2: Performance comparison on the CALVIN ABC-D benchmarks. We report the average number of successfully completed tasks across five consecutive instructions. Bold indicates the best performance*

![[assets/figures/papers/paper_list_l961_https_arxiv_org_abs_2512_09928/figures/012_Table_6.jpg]]
*Table 6: Ablation on different variants. M: Motion, S: State, A: Action. * denotes the submission setting. (third view)*

## 定位与知识库关联

### 问题定位：VLA 时序建模的三种范式

现有视觉-语言-动作模型在应对长程操作任务时，面临一个核心瓶颈：**马尔可夫假设导致的时序近视**——模型仅依据当前观测 $o_t$ 预测动作，忽略了历史动态与未来趋势，使得动作序列缺乏连贯性。围绕这一瓶颈，已有方法大致形成三种范式：

1. **瞬时观测范式**：以 **OpenVLA** 和 **OpenVLA-OFT** 为代表的基线方法，仅输入当前帧进行动作回归或离散令牌预测，无任何显式时序建模。这类方法在短程任务上表现尚可，但在长程任务中因缺乏历史上下文而动作断裂频发。

2. **帧堆叠范式**：通过将多帧历史图像直接拼接作为输入，为模型提供时序信息。然而，原始 RGB 帧携带大量静态像素冗余，导致 GPU 显存和推理延迟随历史长度线性增长（Table 3 显示，历史长度 8 时多帧基线推理延迟超过原始 VLA 的 4.5 倍），且冗余信息分散模型对任务相关动态的注意力。

3. **像素级子目标生成范式**：通过预测未来图像作为子目标来引导动作执行。这类方法虽引入了前向预测，但像素级生成计算代价高昂，且子目标与底层动作之间的映射缺乏结构化约束，难以保证时序一致性。

HiF-VLA 提出的运动表征双向推理范式，正是针对上述三种范式的结构性缺陷进行系统性改进。

### 核心因果机制：运动向量作为时空压缩表征

HiF-VLA 的方法创新根植于一个关键的因果洞察：**运动向量能够紧凑且忠实地捕获状态间的任务相关动态变化，同时滤除静态像素噪声**。具体而言，相邻帧间的运动矢量定义为：

$$MV_{t-1:t}(x,y) = (x_t - x_{t-1}, y_t - y_{t-1})$$

这一低维表征仅编码宏块的位置偏移，将密集的像素级历史压缩为结构化的动态基元，从而在保留时序动态的同时消除冗余。基于此，HiF-VLA 构建了双向时序推理通道：

- **后见先验**：将历史运动向量 $m_{t-h:t}$ 编码为后见令牌 $M_h$，作为条件先验注入动作生成过程，使模型“回顾”已发生的动态。
- **预见推理**：在 VLM 中引入可学习的预见查询令牌，同时预测未来运动 $m_{t:t+n}$ 和动作潜在令牌 $A_f$，实现“边思考边行动”的双流协同。
- **后见调制融合**：通过 AdaLN 条件化和交叉流双向注意力机制，在后见调制联合专家模块中融合 $M_h$、$M_f$ 和 $A_f$，确保动作预测与历史动态及未来趋势因果一致。

### 与基线方法的关键差异槽位

| 设计维度 | OpenVLA / OpenVLA-OFT | HiF-VLA |
|---------|----------------------|---------|
| 时序输入 | 仅当前观测 $o_t$ | 历史运动向量 $m_{t-h:t}$ 经后见编码器产生条件先验 |
| 未来预测 | 无，仅输出动作 | VLM 中联合预测未来运动 $m_{t:t+n}$ 与动作潜在令牌 $A_f$ |
| 融合机制 | 直接使用 VLM 输出经动作头回归 | 后见调制联合专家，采用交叉流双向注意力与 AdaLN 条件化 |
| 动作预测范式 | 仅动作回归 | 联合预测未来运动与动作，形成“边思考边行动”的双流协同 |

### 适用边界与局限

尽管 HiF-VLA 在 LIBERO-Long（96.4% SR）和 CALVIN ABC-D（4.35 Avg.Len.）上取得了显著提升，其方法仍存在明确的适用边界：

1. **3D 空间感知依赖**：真实世界实验中仍出现因空间几何判断和深度估计误差导致的失败（如提前松爪、按压不足），表明当前方法对精确 3D 感知有较强依赖，而运动向量作为 2D 表征无法直接编码深度信息。

2. **预见长度限制**：增加预见长度（如 $n=16$）会导致性能下降，说明单次预测的时序跨度存在上限，长期预测存在误差累积问题。

3. **运动向量提取的格式依赖**：运动向量的提取依赖于视频编码标准（MPEG-4），对训练数据的帧率与格式可能有特定要求，在非标准数据流上的通用性有待验证。

### 开放问题

1. **3D 表示集成**：如何在该框架中有效集成更丰富的 3D 表示（如点云、深度图），以提升空间操作精度，同时保持运动向量的计算高效性？

2. **高级推理扩展**：运动表征目前仅用于动作预测，能否被扩展到更高级的推理任务，如安全性预测、物理规律学习或任务进度监控？

3. **大规模训练稳定性**：在大规模多任务数据上，联合预见与动作的训练范式如何保证收敛稳定性？Figure 7 已初步验证“边思考边行动”可加速运动损失收敛，但在更复杂的数据分布下，双流协同的优化动力学仍需进一步研究。

4. **与基础模型演进的适配**：随着 VLM 基础模型快速迭代，后见调制联合专家的模块化设计能否无缝适配不同架构的 VLM，还是需要针对特定注意力机制进行重新设计？

## 原文 PDF

![[paperPDFs/CVPR_2026/HiF_VLA_Hindsight_Insight_and_Foresight_through_Motion_Representation_for_Vision_Language_Action_Models.pdf]]

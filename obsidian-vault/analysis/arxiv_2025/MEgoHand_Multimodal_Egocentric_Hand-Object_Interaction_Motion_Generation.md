---
title: "MEgoHand: Multimodal Egocentric Hand-Object Interaction Motion Generation"
type: paper
paper_level: A
venue: arXiv
year: 2025
pdf_ref: "paperPDFs/arxiv_2025/MEgoHand:_Multimodal_Egocentric_Hand-Object_Interaction_Motion_Generation.pdf"
project_link: null
code_link: null
aliases:
- MEgoHand
tags:
- arxiv_2025
- topic/motion_animation
- topic/motion_animation/human_motion_generation
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
core_operator: 引入视觉语言模型（VLM）进行运动先验推断，结合单目深度估计实现与物体无关的空间推理，并采用基于DiT的流匹配进行闭环预测，辅以时间正交滤波（TOF）提升时序稳定性，从而摆脱对物体模型和接触图的依赖。
primary_logic: 第一人称手-物交互生成可通过“大模型感知（VLM） + 深度空间推理 + 流匹配闭环生成 + TOF平滑”的统一框架实现，无需显式物体建模，且多模态上下文（RGB、文本、深度）互补可以显著提升泛化性和精细度。
claims:
- MEgoHand 采用双级架构：高层用 VLM 推断运动先验并融合单目深度，低层用 DiT 流匹配生成手部轨迹，并加入 TOF 平滑解码。
- 在域内 5 数据集的平均结果上，MEgoHand 相比 LatentAct 的 MRE 降低 86.9%，MPJPE-PA 降低 71.2%。
- 去除深度监督（仅靠运动预测损失）会导致性能大幅下降，表明必须借助显式深度监督才能学到空间感知表征。
- 在跨域数据集 ARCTIC 和 HOLO 上，MEgoHand 的 MPJPE 相对最强基线分别降低 33.9% 和 29.8% 。
---

# MEgoHand: Multimodal Egocentric Hand-Object Interaction Motion Generation

> [!tip] 核心洞察
> 第一人称手-物交互生成可通过“大模型感知（VLM） + 深度空间推理 + 流匹配闭环生成 + TOF平滑”的统一框架实现，无需显式物体建模，且多模态上下文（RGB、文本、深度）互补可以显著提升泛化性和精细度。

| 字段      | 内容                                                                                         |
| ------- | ------------------------------------------------------------------------------------------ |
| 中文题名    | MEgoHand：多模态第一人称手-物交互运动生成                                                                  |
| 英文题名    | MEgoHand: Multimodal Egocentric Hand-Object Interaction Motion Generation                  |
| 会议/期刊   | arXiv 2025                                                                                 |
| Links | [paper](https://arxiv.org/abs/2505.16602) |
| Topic | #topic/motion_animation #topic/motion_animation/human_motion_generation #topic/vision_multimodal_applications #topic/generative_models_diffusion |
| Method  | MEgoHand                                                                                   |
| Dataset | In-domain, Cross-domain ARCTIC, Cross-domain HOLO                                          |

> [!tip] 效果简介
> - In-domain (avg. over TACO, HOI4D, H2O, HOT3D, OakInk2) 上，MPJPE (cm) 5.425 vs 7.726 (LatentAct) (-2.301 (≈29.8%))。
> - In-domain (avg.) 上，MRE (rad) 0.123 vs 0.937 (LatentAct) (-0.814 (86.9% reduction))。
> - Cross-domain ARCTIC 上，MPJPE (cm) 7.358 vs 10.98 (LatentAct-Diff) (-3.622 (33.9% reduction))。

## 概述

第一人称（egocentric）手-物交互运动生成面临三重结构性挑战：**视角固有的不稳定性**（自遮挡、透视畸变、ego运动噪声）、**对预定义3D物体先验或接触图的强依赖**（难以泛化到新物体），以及**开环预测的累积误差**。现有方法在多模态上下文建模、空间推理和时序一致性方面存在明显瓶颈。

MEgoHand 的核心洞察是：**第一人称手-物交互生成可以通过“大模型感知 + 深度空间推理 + 流匹配闭环生成 + 时序正交滤波”的统一框架实现，无需显式物体建模**。具体而言，该方法采用双级架构——高层利用视觉语言模型（VLM）推断运动先验，并结合单目深度估计实现与物体无关的空间推理；低层基于 DiT（Diffusion Transformer）的流匹配策略进行闭环手部轨迹生成，辅以训练自由的时序正交滤波（TOF）提升时序稳定性。

在域内5个数据集（TACO、HOI4D、H2O、HOT3D、OakInk2）的平均结果上，MEgoHand 相比此前最优方法 **LatentAct**（Prakash et al., arXiv 2025）将平均旋转误差（MRE）降低 **86.9%**（0.937→0.123 rad），将 Procrustes 对齐后的平均关节位置误差（MPJPE-PA）降低 **71.2%**。在跨域数据集 ARCTIC 和 HOLO 上，MPJPE 相对最强基线分别降低 **33.9%** 和 **29.8%**，展现出显著的泛化能力。消融实验进一步证实，**显式深度监督是学习空间感知表征的必要条件**——去除深度监督后，域内 MPJPE 从 5.425 cm 升至 5.725 cm，跨域 ARCTIC 上从 7.358 cm 升至 8.174 cm。

方法层面，MEgoHand 在三个关键维度上区别于现有工作：**视觉编码器**从传统 CNN/Transformer 升级为 VLM（Eagle-2 + SmolLM2 + SigLIP-2），**深度输入**从无到引入单目度量深度估计（UniDepthV2），**运动生成模型**从 Transformer 基架构转向 DiT 基流匹配。为统一多源数据，作者还构建了包含 Inverse MANO Retargeting 网络和 Virtual RGB-D Renderer 的标准化管线，产出约 335 万帧的多模态数据集。

该方法的主要局限在于：对关节物体的复杂动态耦合（如剪刀剪切）泛化不足；度量深度在跨域场景下对相机参数剧烈变化较为敏感；当前仅支持右手交互，尚未扩展到双手场景。

## 背景与动机

第一人称手-物交互运动生成是具身智能与增强现实的核心能力，目标是从自我中心视角的感知输入中预测未来手部运动序列。该任务面临三重结构性困难：

**视角退化与感知歧义。** 第一人称相机的视点随佩戴者运动而剧烈变化，同时引入自遮挡、透视畸变和ego运动噪声。单帧RGB图像缺乏显式的3D空间信息，使得从二维观测推断三维手部姿态本身就是一个病态问题。

**物体先验依赖与泛化瓶颈。** 现有方法普遍依赖预定义的3D物体模型或接触图（contact map）作为空间约束。例如，先前SOTA方法 **LatentAct**（Prakash et al., arXiv 2025）需要接触图作为显式输入来建模手-物关系。这种设计导致模型难以泛化到训练中未见过的物体类别和几何形态。

**多模态融合与开环误差累积。** 现有工作多将文本作为抽象指令嵌入，缺乏对复杂手-物交互语义的深层理解。同时，开环预测框架在长序列生成中会逐步累积姿态误差，导致手部漂移和穿透。

上述瓶颈共同指向一个核心矛盾：高质量的手-物交互生成需要精确的空间推理和语义理解，但第一人称视角的感知退化与物体先验的泛化限制使得现有方法难以兼顾精度与通用性。MEgoHand 的动机正是打破这一僵局——通过引入视觉语言模型（VLM）进行运动先验推断、结合单目深度估计实现与物体无关的空间推理，并采用基于DiT的流匹配进行闭环预测，从而构建一个无需显式物体建模的统一生成框架。

## 核心创新

MEgoHand 的核心创新在于将第一人称手-物交互生成从“依赖显式物体建模与接触图”的范式，转向“大模型感知 + 深度空间推理 + 流匹配闭环生成 + 时序平滑”的统一框架。这一转变通过四个关键 **changed slots** 实现，每个 slot 都对应一个明确的瓶颈突破。

### 1. 视觉编码器：从 CNN/Transformer 到 VLM

**Baseline**：LatentAct（Prakash et al., arXiv 2025）等现有方法使用传统 CNN 或 Transformer 作为视觉编码器，其语义理解能力受限于训练数据和模型容量，难以从第一人称视角的复杂场景中提取丰富的交互上下文。

**Proposed**：MEgoHand 采用 **Eagle-2** 视觉语言模型作为核心感知模块，该 VLM 集成了 **SmolLM2** 语言骨干和 **SigLIP-2** 视觉编码器。VLM 在推理阶段保持冻结，仅微调其视觉编码器部分，使其能够利用大规模预训练中习得的语义先验来推断运动意图和交互模式。这一替换使得模型可以直接从 RGB 图像和文本指令中理解“正在发生什么交互”以及“接下来应该做什么”，而无需预定义的物体类别或接触图。

**因果机制**：VLM 的引入将高层运动先验推断从“视觉特征匹配”升级为“语义推理”，这是摆脱物体模型依赖的关键一步。

### 2. 深度输入：从无深度到单目度量深度

**Baseline**：LatentAct 等基线方法不使用深度图，或仅隐式依赖 RGB 中的深度线索，导致空间推理能力薄弱，尤其在自遮挡和透视畸变严重的第一人称视角下。

**Proposed**：MEgoHand 引入 **UniDepthV2** 单目度量深度估计器，从每帧 RGB 图像生成度量深度图，并通过 **ResNet-50** 深度编码器将其编码为特征。深度特征与 VLM 视觉特征通过 **加性融合模块** 组合，形成统一的视觉-空间表征。训练时对深度编码器施加显式深度监督损失，强制模型学习空间感知表征。

**因果机制**：度量深度提供了与物体无关的 3D 空间线索，使模型能够在不建模物体几何的情况下推断手部相对于场景的位姿和运动轨迹。消融实验证实，去除深度监督会导致域内 MPJPE 从 5.425 cm 升至 5.725 cm，跨域 ARCTIC 上从 7.358 cm 升至 8.174 cm，表明显式深度监督是学习空间表征的必要条件。

### 3. 运动生成模型：从 Transformer/Diffusion 到 DiT 流匹配 + TOF

**Baseline**：LatentAct 使用 Transformer 或扩散模型进行开环运动预测，缺乏对预测误差的闭环修正能力，且时序一致性较弱。

**Proposed**：MEgoHand 采用 **DiT（Diffusion Transformer）基的流匹配** 模型作为运动生成器。该模型接收多模态表征和初始手部参数 $h_k$，通过条件流匹配损失 $\mathcal{L}^\tau(\boldsymbol{\theta})$ 学习从噪声到数据的向量场 $\nu_\theta$，推理时通过前向欧拉积分从 $\tau=0$ 到 $\tau=1$ 逐步生成未来 $l$ 步的 MANO 参数序列 $\mathcal{H}_k$。此外，引入 **时间正交滤波（TOF）** 作为训练自由的平滑解码策略：对重叠预测窗口内的平移取平均，对旋转矩阵通过 SVD 投影到 SO(3) 实现平滑，有效抑制轨迹抖动。

**因果机制**：DiT 流匹配提供了闭环生成能力，每一步预测都以前一步的生成结果为条件，减少了开环累积误差。TOF 则在不增加训练成本的前提下提升了时序稳定性。

### 4. 数据统一：从标注不一致到标准化多模态数据集

**Baseline**：现有第一人称 HOI 数据集标注格式各异，缺乏对齐的深度信息，难以联合训练。

**Proposed**：MEgoHand 设计了两项数据统一工具：**Inverse MANO Retargeting Network** 从关节坐标恢复 MANO 参数，统一不同数据集的姿态表示；**Virtual RGB-D Renderer** 利用 MANO 模型和相机参数合成与 RGB 对齐的深度图，补充缺失的深度信息。由此构建了包含 3.35M RGB-D 帧、24K 交互轨迹、覆盖 1.2K 物体的统一多模态数据集。

**因果机制**：数据统一使得多数据集联合训练成为可能，显著提升了模型的泛化能力——这是跨域零样本迁移性能（ARCTIC 上 MPJPE 降低 33.9%，HOLO 上降低 29.8%）的基础。

### 创新总结

四个 changed slots 形成了一条完整的因果链：**VLM 提供语义先验 → 深度估计提供空间推理 → DiT 流匹配实现闭环生成 → TOF 保证时序平滑**。这一链条使得 MEgoHand 在无需任何物体模型或接触图的前提下，相比前 SOTA LatentAct 实现了 MRE 降低 86.9%、MPJPE-PA 降低 71.2% 的显著提升。

## 整体框架

MEgoHand 的整体推理管线可概括为 **“高层语义推理 + 低层运动生成 + 时序平滑解码”** 的双级架构，其输入输出流如下：

1. **输入**：任务文本描述 $\mathcal{T}$、当前时刻的视觉观测 $\mathcal{V}_k$（RGB 图像）以及初始手部参数 $h_k \in \mathbb{R}^{109}$（MANO 参数向量，拼接手指旋转 $\theta$、形状 $\beta$、手腕旋转 $r$ 和平移 $t$）。
2. **高层语义与空间推理**：系统提示词与任务指令经冻结的 VLM tokenizer 编码为文本嵌入；同时，RGB 图像通过预训练的单目深度估计器 **UniDepthV2** 获得度量深度图，再经 **ResNet-50** 编码为深度特征。视觉特征与深度特征通过 **加性融合模块** 合并后，送入冻结的 VLM（**Eagle-2**，语言骨干 **SmolLM2**，视觉编码器 **SigLIP-2**）进行运动先验推断，输出多模态表征。
3. **低层运动生成**：多模态表征连同初始手部参数 $h_k$ 一起输入基于 **DiT** 的条件流匹配运动生成器，通过积分学习到的向量场 $\nu_\theta$ 从噪声逐步生成未来 $l$ 步的相对手部运动序列 $\mathcal{H}_k = \{h_{k+1}, h_{k+2}, \dots, h_{k+l}\}$。
4. **时序平滑解码**：生成的序列经 **时间正交滤波（TOF）** 进行训练自由的平滑处理——平移量通过滑动窗口平均，旋转矩阵通过 SVD 投影到 SO(3) 流形上——以消除逐帧预测的抖动，增强时序一致性。
5. **输出**：平滑后的未来手部 MANO 参数序列，可直接驱动手部网格渲染。

该管线的核心设计意图是**摆脱对显式 3D 物体模型和预定义接触图的依赖**：VLM 提供对任务语义和手-物关系的上下文理解，单目深度估计赋予与物体无关的空间感知能力，DiT 流匹配实现闭环预测，TOF 则补偿开环生成带来的累积误差。训练时仅微调解冻的深度编码器、VLM 视觉编码器和 DiT 头，VLM 语言骨干保持冻结。

为支撑上述管线，作者构建了统一的多模态数据集管线：通过 **Inverse MANO Retargeting Network** 将各数据集的异构关节点标注统一恢复为 MANO 参数，并通过 **Virtual RGB-D Renderer** 合成与 RGB 对齐的深度图，最终形成覆盖 3.35M 帧 RGB-D、24K 条交互轨迹、1.2K 物体的训练集。

> **证据强度说明**：上述模块关系与数据流在 Section 3.1–3.3 及 Figure 2 中有明确描述（置信度 0.95）；Inverse MANO Retargeting 与 Virtual RGB-D Renderer 的数据统一作用见 Section 4（置信度 0.9）。具体模块名称与骨干网络选择均来自原文锚点，无推测成分。

![[assets/figures/papers/paper_list_l7_https_arxiv_org_abs_2505_16602/figures/002_Figure_2.jpg]]
*Figure 2: During inference, the system prompt and task instruction are encoded using a frozen VLM tokenizer. At each timestep, an RGB image is processed by a pretrained depth estimator to obtain a metric depth map. The RGB and depth images are then combined and encoded into a visual embedding, which—together with the text embedding—is input to the frozen VLM. A DiT-based motion generator receives this multimodal representation along with the initial hand parameters to predict relative future hand motion. During training, the depth encoder, VLM vision encoder, and DiT head are finetuned*

## 核心模块与公式推导

### 问题形式化

MEgoHand 将第一人称手-物交互运动生成形式化为一个条件预测问题。给定任务文本描述 $\mathcal{T}$、当前时刻的视觉观测 $\mathcal{V}_k$（RGB图像）以及初始手部参数 $h_k$，模型预测未来 $l$ 步的 MANO 手部参数序列：

$$\mathcal{H}_k = \{ h_{k+1}, h_{k+2}, \ldots, h_{k+l} \} = \mathrm{MEgoHand}(\mathcal{T}, \mathcal{V}_k, h_k)$$

其中 MANO 手部参数向量 $h \in \mathbb{R}^{109}$ 由四部分拼接而成：

$$h = [\theta ; \beta ; r ; t]$$

- $\theta$：15 个手指关节的旋转参数，以 6D 连续表示编码，共 $15 \times 6 = 90$ 维
- $\beta$：手部形状参数，10 维
- $r$：手腕全局旋转，6 维 6D 表示
- $t$：手腕平移，3 维

### 高层感知模块：VLM 与深度空间推理

**VLM 骨干网络。** 高层模块的核心是视觉语言模型 **Eagle-2**，其集成了 **SmolLM2** 语言骨干和 **SigLIP-2** 视觉编码器。在推理时，系统提示词和任务指令通过冻结的 VLM tokenizer 编码为文本嵌入。VLM 的作用是从 RGB 图像和文本指令中推断高层运动先验——例如当前正在执行的动作阶段、手与物体的语义关系等，而非直接回归精确的关节角度。

**单目深度估计。** 为弥补纯 RGB 输入在 3D 空间推理上的不足，MEgoHand 引入预训练的单目深度估计器 **UniDepthV2**，从每一帧 RGB 图像估计度量深度图。深度图提供了与物体无关的空间距离线索，使模型无需依赖预定义的 3D 物体模型即可感知手-物接触的几何关系。

**特征融合。** RGB 图像和深度图分别经过视觉编码后，通过 **Additive Fusion Module** 进行相加融合，生成统一的视觉嵌入。该嵌入与文本嵌入一起输入冻结的 VLM，最终输出多模态表征 $z_k^{TDI}$（Text-Depth-Image），作为低层运动生成器的条件信号。

### 低层运动生成模块：DiT 流匹配

低层模块采用基于 **DiT（Diffusion Transformer）** 的流匹配框架生成未来手部运动序列。与扩散模型不同，流匹配直接学习从简单噪声分布到目标数据分布的条件概率路径上的向量场。

**条件流匹配损失。** 训练目标是让向量场 $\nu_{\theta}$ 逼近从噪声样本 $\mathcal{H}_k^\tau$ 到真实运动 $\mathcal{H}_k$ 的条件概率路径方向 $\mathbf{u}$：

$$\mathcal{L}^\tau(\boldsymbol{\theta}) = \mathbb{E}_{p(\mathcal{H}_k|h_k, z_k^{TDI}),\, q(\mathcal{H}_k^\tau|\mathcal{H}_k)} \left[ \| \nu_{\boldsymbol{\theta}}(\mathcal{H}_k^\tau, h_k, z_k^{TDI}) - \mathbf{u}(\mathcal{H}_k^\tau|\mathcal{H}_k) \|^2 \right]$$

其中 $\tau \in [0, 1]$ 表示从噪声（$\tau=0$）到数据（$\tau=1$）的时间步，$q(\mathcal{H}_k^\tau|\mathcal{H}_k)$ 定义了插值路径上的条件分布。

**推理时的前向欧拉积分。** 生成过程从随机噪声 $\mathcal{H}_k^0$ 出发，通过逐步积分学习到的向量场得到运动序列：

$$\mathcal{H}_k^{\tau + \delta} = \mathcal{H}_k^\tau + \delta \cdot \nu_{\theta}(\mathcal{H}_k^\tau, h_k, z_k^{TDI})$$

其中 $\delta$ 为积分步长。从 $\tau=0$ 积分到 $\tau=1$ 即可获得最终预测的运动序列。

### 时序正交滤波（TOF）平滑解码

流匹配的逐 chunk 预测会导致相邻 chunk 之间的运动轨迹出现抖动。MEgoHand 提出一种**无需训练的 TOF 解码策略**，通过平均重叠预测窗口内的平移和旋转来抑制高频噪声。

**平移平滑。** 对每个时刻 $k$ 的预测平移 $\hat{t}_k$，取长度为 $l$ 的滑动窗口内的均值：

$$\tilde{t}_k = \frac{1}{l} \sum_{t=1}^l \hat{t}_k^{k-t}$$

**旋转平滑与 SO(3) 投影。** 旋转矩阵的简单平均会破坏正交性。TOF 先计算窗口内旋转矩阵的算术平均 $\bar{R}_k$，再通过 SVD 分解投影回 SO(3) 流形：

$$\tilde{R}_k = \arg\min_{R \in SO(3)} \| R - \bar{R}_k \|_F = UV^\top, \quad \text{其中 } USV^\top = \mathrm{SVD}(\bar{R}_k)$$

该策略在附录消融中展示了显著的去抖效果：未使用 TOF 时预测轨迹存在明显的高频波动，加入 TOF 后运动曲线趋于平滑。

### 数据统一化：逆向 MANO 重定向

为整合来自不同数据集的异构标注（部分数据集仅有 3D 关节坐标而无 MANO 参数），MEgoHand 训练了一个**逆向 MANO 重定向网络 $\phi$**，从关节坐标恢复 MANO 参数。训练采用两阶段策略：

$$\mathcal{L}_1 = w_1 \mathcal{L}_{\mathrm{shape}}(\phi(j), \theta, \beta) + \mathcal{L}_{\mathrm{recon}}(\mathbf{MANO}(\phi(j)), j)$$

$$\mathcal{L}_2 = w_2 \mathcal{L}_{\mathrm{pose}}(\phi(j), r, t) + \mathcal{L}_{\mathrm{recon}}(\ldots)$$

$$\mathcal{L}_{\mathrm{inv}} = \sigma \mathcal{L}_1 + (1-\sigma) \mathcal{L}_2$$

第一阶段（$\sigma=1$）优化手部形状参数 $\theta, \beta$，第二阶段（$\sigma=0$）固定形状后优化手腕姿态 $r, t$。这种解耦训练策略避免了形状和姿态参数的联合优化陷入局部极小。

### 虚拟 RGB-D 渲染

对于缺少深度标注的数据集，MEgoHand 利用 MANO 模型和已知相机参数，将逆向重定向恢复的手部网格投影到图像平面，合成与 RGB 对齐的深度图。渲染时采用最近表面保留策略 $D[v,u] = \min(D[v,u], Z_c^{(i)})$，确保深度图中只保留离相机最近的手部表面。这一步骤使所有训练数据统一为 RGB-D-文本-姿态四元组格式，最终构建了包含 335 万帧、2.4 万条交互轨迹、覆盖 1200 个物体的多模态数据集。

### 补充图表

![[assets/figures/papers/paper_list_l7_https_arxiv_org_abs_2505_16602/figures/012_Figure_2.jpg]]
*Figure 2: Illustration for smoothing predicted transformations*

![[assets/figures/papers/paper_list_l7_https_arxiv_org_abs_2505_16602/figures/015_Figure_4.jpg]]
*Figure 4: Colorbars indicate the absolute depth values (unit: m). The depth values of all depth frames fall within [0, 2]*

## 实验与分析

### 评估设置

MEgoHand 在五个域内数据集（TACO、HOI4D、H2O、HOT3D、OakInk2）和两个跨域数据集（ARCTIC、HOLO）上进行评估。主要指标包括：

- **MPJPE (cm)**：预测与真值 3D 手部关节位置的平均欧氏距离。
- **MPJPE-PA (cm)**：经 Procrustes 对齐后的 MPJPE。
- **MPVE-PA (cm)**：经 Procrustes 对齐后的手部网格顶点误差。
- **MRE (rad)**：16 关节（1 腕 + 15 指）预测与真值旋转矩阵的平均角度误差，定义为 $\mathrm{MRE} = \frac{1}{16} \sum_{j=1}^{16} \cos^{-1}\left( \frac{\mathrm{trace}(R_{1,j}^T R_{2,j}) - 1}{2} \right)$。

所有方法使用相同的初始手部姿态，并将 LatentAct 的运动预测对齐到每个 chunk 的第一帧以保证公平比较。FPHA 数据集通过 Inverse MANO 重新标注且仅用于评估。训练/评估按动作类别和物体类别划分，无重叠。

### 域内评估

Table 1 展示了五个域内数据集的平均结果。MEgoHand 在所有指标上均大幅超越基线方法 LatentAct（Prakash et al., arXiv 2025）：

![[assets/figures/papers/paper_list_l7_https_arxiv_org_abs_2505_16602/figures/005_Table_1.jpg]]
*Table 1: Average metrics of in-domain evaluation across 5 datasets: TACO, HOI4D, H2O, HOT3D, and OakInk2. The unit for MRE is radians, and the remaining metrics are measured in centimeters*

![[assets/figures/papers/paper_list_l7_https_arxiv_org_abs_2505_16602/figures/010_Table_1.jpg]]
*Table 1: Hyperparameters of MEgoHand Training*

- **MRE**：0.123 rad vs. 0.937 rad，相对降低 **86.9%**。这是最显著的提升，表明 MEgoHand 在关节旋转预测上远优于依赖接触图的 LatentAct。
- **MPJPE**：5.425 cm vs. 7.726 cm，降低约 29.8%。
- **MPJPE-PA**：0.425 cm vs. 1.478 cm，相对改善 **71.2%**。
- **MPVE-PA**：0.409 cm vs. 1.453 cm，相对改善 **71.9%**。

经 Procrustes 对齐后，关节误差和网格顶点误差分别降至 0.424 cm 和 0.409 cm，表明 MEgoHand 在消除全局姿态歧义后能够以亚厘米精度恢复手部姿态。

### 跨域零样本迁移

Table 2 展示了在未见过数据集上的零样本泛化能力。MEgoHand 相比最强基线 LatentAct-Diff 取得一致且显著的提升：

![[assets/figures/papers/paper_list_l7_https_arxiv_org_abs_2505_16602/figures/007_Table_2.jpg]]
*Table 2: Average metrics of out-of-domain evaluation across 2 datasets: ARCTIC and HOLO. The unit for MRE is radians, and the remaining metrics are measured in centimeters*

![[assets/figures/papers/paper_list_l7_https_arxiv_org_abs_2505_16602/figures/016_Table_2.jpg]]
*Table 2: Average metrics across evaluation (TACO, HOI4D, H2O, HOT3D, OakInk2) and testing datasets (ARCTIC, HOLO). The unit for MRE is radians; the remaining metrics are measured in centimeters*

- **ARCTIC**：MPJPE 7.358 cm vs. 10.98 cm，降低 **33.9%**。
- **HOLO**：MPJPE 5.775 cm vs. 9.550 cm，降低 **29.8%**（与论文声明一致）。

这些结果表明，MEgoHand 通过 VLM 语义理解和深度空间推理，能够泛化到训练时未见过的相机配置、物体类别和交互场景，而无需依赖预定义的物体模型。

### 消融实验

Table 3 的消融研究揭示了关键设计选择的影响：

![[assets/figures/papers/paper_list_l7_https_arxiv_org_abs_2505_16602/figures/008_Table_3.jpg]]
*Table 3: The ablation studies of MEgoHandvariants across evaluation datasets and test datasets*

**深度监督的必要性**：去除显式深度监督（仅靠运动预测损失更新深度编码器）导致性能显著下降——域内 MPJPE 从 5.425 cm 升至 5.725 cm，ARCTIC 跨域 MPJPE 从 7.358 cm 升至 8.174 cm。这证明显式深度监督是学习空间感知表征的必要条件，而非可有可无的辅助信号。

**深度估计器的即插即用兼容性**：将默认的 UniDepthV2 替换为 DepthAnythingV2 或使用相对深度，性能保持相近。这表明方法对不同深度估计器具有良好的鲁棒性，不依赖于特定深度模型的特性。

**度量深度 vs. 相对深度**：度量深度在域内场景提供一致的尺度和距离线索，有利于 3D 空间理解；但在跨域场景下对相机参数剧烈变化更敏感，可能导致性能下降。这一发现揭示了度量深度在泛化场景中的双刃剑效应。

### 定性分析

Figure 5 和 Figure 6 展示了 MEgoHand 与 LatentAct 在域内（绿色）和跨域（蓝色）数据集上的手部网格投影对比。MEgoHand 生成的手部姿态与图像中的物体交互区域更加吻合，尤其在存在自遮挡和透视畸变的第一人称视角下。标注中的对齐误差主要归因于标注噪声和相机标定误差，而非方法本身。

![[assets/figures/papers/paper_list_l7_https_arxiv_org_abs_2505_16602/figures/009_Figure_5.jpg]]
*Figure 5: We present visualizations across in-domain (green) and cross-domain (blue) datasets. The misalignments of ground-truth annotations are attributed to labeling noise and camera calibration errors. For fair comparison with LatentAct, we provide the initial hand pose and align the motion predictions of LatentAct to the first frame in a chunk*

![[assets/figures/papers/paper_list_l7_https_arxiv_org_abs_2505_16602/figures/017_Figure_5.jpg]]
*Figure 5: Additional visualizations of LatentAct and MEgoHand. Green part is sampled from training sets. Blue part is sampled from evaluation sets. The Yellow part is sampled from testing sets*

![[assets/figures/papers/paper_list_l7_https_arxiv_org_abs_2505_16602/figures/018_Figure_6.jpg]]
*Figure 6: Additional visualizations of LatentAct and MEgoHand. Green part is sampled from training sets. Blue part is sampled from evaluation sets. The Yellow part is sampled from testing sets*

Figure A.3 展示了 TOF 平滑解码策略对轨迹抖动的抑制效果：在 TACO 数据集“用铲子搅拌碗”任务中，不使用 TOF 的预测轨迹表现出明显的高频抖动，而 TOF 通过重叠预测的平均平移和 SVD 投影到 SO(3) 的旋转平滑，显著提升了时序一致性。

### 失败模式与局限

1. **关节物体动态耦合**：在涉及剪刀剪切等复杂关节物体交互时，模型泛化能力不足。这源于训练数据以刚性物体为主，模型缺乏对多刚体运动链耦合的先验。
2. **度量深度的跨域敏感性**：如消融实验所示，度量深度在相机参数剧烈变化的跨域场景中可能导致性能下降，这是当前框架的一个系统性脆弱点。
3. **单手限制**：当前仅支持右手交互生成，尚未扩展到双手交互场景，限制了在需要双手协调的任务上的应用。

### 关键图表指引

| 图表 | 核心结论 |
|------|---------|
| Table 1 | MEgoHand 域内 MRE 降低 86.9%，MPJPE-PA 降低 71.2% |
| Table 2 | 跨域 MPJPE 相对最强基线降低 33.9%（ARCTIC）和 29.8%（HOLO） |
| Table 3 | 去除深度监督导致域内/跨域性能均显著下降；深度估计器可即插即用 |
| Figure 4 | 域内和跨域数据集上 MPJPE 的直观对比 |
| Figure 5/6 | 手部网格投影定性对比，MEgoHand 与物体交互区域更吻合 |

![[assets/figures/papers/paper_list_l7_https_arxiv_org_abs_2505_16602/figures/006_Figure_4.jpg]]
*Figure 4: The evaluation of our two methods and two baseline variants on five in-domain (H2O, HOI4D, HOT3D, OAKINK2, TACO) and two cross-domain datasets (ARCTIC, HOLO), using MPJPE as metric (unit: cm, lower is better)*

## 方法谱系与知识库定位

### 与现有基线的关键差异

MEgoHand 与先前第一人称手部运动生成方法的核心分歧在于**是否依赖显式物体先验**。以 **LatentAct**（Prakash et al., arXiv 2025）为代表的现有 SOTA 需要接触图（contact map）作为中间表示，这隐含了对物体几何的依赖，导致泛化到新物体时性能急剧退化。MEgoHand 通过三个结构性替换切断了这一依赖链：

1. **视觉编码器**：从传统 CNN/Transformer 替换为视觉语言模型（VLM）**Eagle-2**，其语言骨干为 **SmolLM2**，视觉编码器为 **SigLIP-2**。VLM 不仅编码视觉外观，更从任务文本和系统提示中推断运动先验——例如“拿起杯子”与“搅拌碗中液体”对手指姿态和时序的要求截然不同，VLM 可直接从语义层面捕捉这一差异，无需接触图作为代理。

2. **深度输入**：引入单目度量深度估计器 **UniDepthV2**，并通过 **ResNet-50** 编码深度特征，经加法融合模块与视觉特征结合。这使模型获得与物体无关的 3D 空间感知能力——深度图直接提供手与场景表面的距离线索，而非通过物体模型间接推断。消融实验（Table 3）证实：去除显式深度监督后，域内 MPJPE 从 5.425 cm 恶化至 5.725 cm，跨域 ARCTIC 上从 7.358 cm 恶化至 8.174 cm，表明深度监督是学习空间表征的**必要条件**而非辅助信息。

3. **运动生成模型**：从 Transformer 基或扩散模型替换为基于 **DiT（Diffusion Transformer）的流匹配**框架，并辅以**时间正交滤波（TOF）**解码。DiT 流匹配提供闭环预测能力，TOF 通过对重叠预测窗口的平移取平均、旋转经 SVD 投影到 SO(3) 流形，实现训练自由的时序平滑，显著抑制开环预测的累积误差和轨迹抖动。

### 适用边界与局限

**刚性物体交互为主**。训练数据覆盖 1.2K 物体，但以刚性物体占主导。在涉及关节物体的复杂动态耦合场景（如剪刀剪切）中，模型泛化能力不足——这是因为关节物体的运动自由度与手部姿态之间存在更复杂的双向约束，而训练分布未能充分覆盖此类模式。

**右手交互单侧支持**。当前框架仅生成右手运动序列，尚未扩展到双手协同交互。双手场景不仅需要处理双手各自的运动生成，还需建模双手间的协调约束和力传递，这对 VLM 的空间推理和 DiT 的条件生成均提出更高要求。

**跨域深度敏感性**。度量深度在域内场景提供一致的尺度和距离线索，有利于 3D 空间理解；但在跨域场景下，当相机内参、外参或场景尺度发生剧烈变化时，度量深度估计的绝对误差会被放大，导致性能下降。消融实验（Table 3）显示替换为相对深度估计器可获得相近性能，表明深度模态的“即插即用”兼容性良好，但度量深度的跨域鲁棒性仍是瓶颈。

### 在知识库中的定位

从方法谱系看，MEgoHand 处于**多模态条件生成 × 第一人称手-物交互 × 大模型感知**的交汇点：

- **相对于接触图方法**（如 LatentAct）：MEgoHand 证明了“VLM 语义推理 + 深度空间感知”可以替代显式接触图，且泛化性显著更优（域内 MRE 降低 86.9%，跨域 MPJPE 降低 29.8%–33.9%）。这为摆脱物体模型依赖的 HOI 生成提供了新范式。

- **相对于纯视觉运动生成**：通过引入文本任务描述作为条件，MEgoHand 将运动生成从“观察-模仿”提升为“理解-执行”，使同一视觉观测下可根据不同任务指令生成不同的手部运动（例如同一初始手部姿态下，“抓取”与“推动”的动作序列应截然不同）。

- **相对于大模型直接预测运动**：MEgoHand 采用“VLM 高层推理 + DiT 低层精化”的双级架构，而非端到端让 VLM 输出运动参数。这一设计避免了 VLM 在连续运动空间中的生成精度不足问题，同时保留了其语义理解优势。

### 开放问题

1. **数据规模扩展**。预训练的 Inverse MANO Retargeting 网络可将任意关节坐标标注转换为统一的 MANO 参数格式，理论上可用于标注更广泛的 HOI 数据集甚至自然场景视频。现代手部姿态检测器若能提供足够精度的关节坐标，则可大幅扩展训练数据规模和场景多样性，缓解关节物体交互等长尾场景的覆盖不足。

2. **跨域深度鲁棒性**。如何缓解度量深度在跨域时的相机参数敏感性？可能的路径包括：在深度编码器中引入相机参数条件化、采用深度归一化策略消除绝对尺度依赖、或联合优化深度估计与运动生成的域自适应训练。

3. **双手交互扩展**。将框架从单手扩展到双手需要解决的核心问题包括：VLM 如何同时推理双手的任务角色分配、DiT 如何生成双手的协调运动序列、以及 TOF 如何在双手间保持相对位姿的一致性。

## 原文 PDF

![[paperPDFs/arxiv_2025/MEgoHand:_Multimodal_Egocentric_Hand-Object_Interaction_Motion_Generation.pdf]]

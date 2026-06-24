---
title: "CoMo: Learning Continuous Latent Motion from Internet Videos for Scalable Robot Learning"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/CoMo_Learning_Continuous_Latent_Motion_from_Internet_Videos_for_Scalable_Robot_Learning.pdf
project_link: null
code_link: "https://github.com/MCG-NJU/CoMo"
aliases:
- CoMo
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 通过早期时序差分机制（Td）消除未来帧特征输入并增强运动线索，同时辅以时序对比学习（Tcl）强制潜在运动关注有意义的运动模式并抑制背景噪声，二者协同作用使得连续潜在运动既连续又动作相关。
primary_logic: 去除向量量化并采用Td与Tcl相结合的策略，能够在不牺牲信息完整性的前提下有效缓解shortcut learning，学得的连续潜在运动不仅保留了细粒度动态信息，还与机器人动作空间保持一致的连续分布，从而直接赋能统一策略的联合训练。
claims:
- Td和Tcl协同作用使CoMo在LIBERO上的平均成功率（80.1%）显著优于离散基线（75.9%）和朴素连续基线（75.2%），且MSE和S-PCFC指标均最优。
- 引入CoMo伪动作标签的联合训练将LIBERO成功率从仅使用机器人数据的70.4%提升至80.1% (Table 3)，并在CALVIN上将平均完成跨度从1.878提升至3.070 (Table 2)。
- 可视化表明，仅Td可消除背景噪声，但运动表征稀疏；增加Tcl使运动更聚焦前景、更结构化，预测的未来帧更准确地反映细粒度动作变化。
- LIBERO (四合一平均) 上 平均成功率 ↑ = 80.1 (CoMo)
---

# CoMo: Learning Continuous Latent Motion from Internet Videos for Scalable Robot Learning

> [!tip] 核心洞察
> 去除向量量化并采用Td与Tcl相结合的策略，能够在不牺牲信息完整性的前提下有效缓解shortcut learning，学得的连续潜在运动不仅保留了细粒度动态信息，还与机器人动作空间保持一致的连续分布，从而直接赋能统一策略的联合训练。

| 字段 | 内容 |
|------|------|
| 中文题名 | CoMo：从互联网视频中学习连续潜在运动以实现可扩展的机器人学习 |
| 英文题名 | CoMo: Learning Continuous Latent Motion from Internet Videos for Scalable Robot Learning |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2505.17006) · [Code](https://github.com/MCG-NJU/CoMo) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/vision_multimodal_applications/image_and_video_generation |
| Method | CoMo |
| Dataset | LIBERO, CALVIN |

> [!tip] 效果简介
> - LIBERO (四合一平均) 上，平均成功率 ↑ 80.1 (CoMo) vs 70.4 (DP w/o videos) (+9.7)；平均成功率 ↑ 80.1 (CoMo) vs 75.9 (Dis. / GR00T style) (+4.2)；Action Prediction MSE ↓ 1.2588 (CoMo) vs 5.6743 (Dis.) (-4.4155)。
> - CALVIN (ABC→D) 上，平均成功序列长度 ↑ 3.070 (CoMo) vs 1.878 (w/o Motion) (+1.192)。

## 概述

**问题瓶颈**：从互联网视频中无监督学习连续潜在运动面临严重的shortcut learning——模型倾向于捕获静态背景信息而非前景运动，导致潜在运动包含大量动作无关噪声，无法为机器人策略提供有效的伪动作标签。

**核心方案**：CoMo提出两条协同机制来破解这一瓶颈：(1) **早期时序差分（Td）**——通过移除未来帧特征输入并计算帧间特征差，增加shortcut学习难度并显式增强运动线索；(2) **时序对比学习（Tcl）**——以微小未来偏移构造正运动对、以时序反转构造负运动对，强制潜在运动聚焦有意义的前景区域并抑制背景噪声。二者协同使得连续潜在运动既保留细粒度动态信息，又与机器人动作空间保持一致的连续分布。

**主要结果**：在LIBERO基准上，仅使用10条机器人示范轨迹（典型设置的1/5），CoMo的平均成功率达80.1%，显著优于不使用视频的基础扩散策略（70.4%）和离散潜在运动基线（75.9%）；在CALVIN ABC→D上，平均完成跨度从1.878提升至3.070。可视化与消融实验进一步证实，Td有效消除背景噪声，Tcl使运动表征更聚焦前景、更结构化。

**方法定位**：CoMo属于基于逆动力学-前向动力学（IDM-FDM）范式的自监督潜在运动学习方法，去除向量量化以输出连续潜在运动，并引入Td与Tcl协同缓解shortcut learning。该方法与**ATM**（Wen et al., RSS 2024）的任意点轨迹建模、**Dynamo**（Cui et al., NeurIPS 2024）的协方差正则化等方案形成互补，在连续潜在运动质量与下游策略性能上展现出系统性优势。

## 背景与动机

### 机器人学习的数据瓶颈与互联网视频的潜力

机器人策略学习长期受限于高质量动作标注数据的稀缺。获取机器人示范需要昂贵的硬件部署和人工遥操作，导致数据规模远无法匹敌自然语言处理或计算机视觉领域。一个自然的思路是借助海量互联网视频——这些视频天然包含丰富的人类或机器人操作行为，且无需动作标注即可大规模获取。然而，如何从这些“无动作”视频中提取有效的运动信号来辅助机器人策略学习，始终是一个开放难题。

### 现有方法的两难困境：离散量化与连续表征的取舍

从无动作视频中学习运动表征的主流范式是逆动力学模型（Inverse Dynamics Model, IDM）：给定当前帧和未来帧，预测二者之间的潜在运动表征。为防止模型“走捷径”——即仅依赖静态背景信息而非真实前景运动来重建未来帧——已有方法普遍采用向量量化（VQ-VAE）将潜在运动约束为离散码字。这种强信息瓶颈虽能部分抑制shortcut learning，却带来了两个根本性缺陷：

1. **信息损失与分布失配**：小码本（如8或16）的离散表征不可避免地丢弃了细粒度运动动态，导致运动预测的均方误差（MSE）居高不下（如离散基线MSE高达5.6743），且离散分布与机器人连续动作空间存在本质失配，限制了联合训练的效能。
2. **维度扩展困难**：增大码本尺寸可缓解信息损失，但会削弱VQ-VAE对shortcut的抑制作用，使模型重新陷入背景噪声的陷阱。

朴素连续潜在运动方法（去除量化）虽能保留完整信息，但shortcut learning问题急剧恶化：模型倾向于将静态背景编码为“运动”，导致潜在运动包含大量动作无关噪声。这构成了一个根本性的两难——**离散化抑制噪声但损失信息，连续化保留信息但引入噪声**。

### 本文动机：实现连续、精确且动作相关的潜在运动学习

本文的核心洞察在于：**shortcut learning的根源并非连续表征本身，而是模型缺乏足够的约束来区分前景运动与背景噪声**。若能通过精巧的架构设计和训练策略，在保持连续表征信息完整性的同时强制模型聚焦于有意义的运动模式，则连续潜在运动不仅可行，且天然优于离散方案——因其与机器人动作空间共享连续分布，可直接赋能统一策略的联合训练。

基于此，CoMo提出两条互补的技术路线：
- **早期时序差分（Td）**：通过显式移除未来帧特征输入并注入帧间差分信号，从根源上增加shortcut难度并增强运动线索；
- **时序对比学习（Tcl）**：通过构造正负运动对的对比损失，强制潜在运动在表征空间中形成结构化分布，进一步抑制残余背景噪声。

二者的协同作用使得CoMo能够在无向量量化的前提下，学得既连续又动作相关的潜在运动，从而突破离散方法的性能上限。

## 核心创新

CoMo 的核心创新在于**彻底移除向量量化（VQ）**，转而通过**早期时序差分（Td）**与**时序对比学习（Tcl）**的协同设计，使模型能够从无动作标注的互联网视频中学习到既连续又与动作相关的潜在运动表征。这一设计直接回应了连续潜在运动学习中普遍存在的 shortcut learning 瓶颈——朴素连续模型倾向于捕获静态背景信息而非前景运动，导致潜在运动包含大量动作无关噪声。

### 关键变更槽位

**1. 量化方式：从离散码本到连续潜在空间**

先前方法（如 GR00T、Moto）依赖 VQ-VAE 将帧间运动压缩至小规模离散码本（如 8 或 16），虽能缓解 shortcut learning，但代价是严重的信息损失。CoMo 去除向量量化约束，输出维度可扩展（128–512）的连续潜在运动表征。这一变更的核心动机在于：连续潜在空间与机器人动作空间的连续分布天然一致，能够保留更细粒度的动态信息，从而为统一策略的联合训练提供更高质量的伪动作标签。实验证据表明，离散基线在 LIBERO 上的动作预测 MSE 高达 5.6743，而 CoMo 仅为 1.2588（Table 1），信息保留优势显著。

**2. 逆动力学编码器输入：移除未来帧特征，引入时序差分**

朴素连续基线直接编码当前帧特征 $F_t$ 与未来帧特征 $F_{t+n}$，这为模型提供了通过静态背景匹配来“走捷径”的便利。CoMo 显式移除未来帧特征 $F_{t+n}$，代之以时序差分特征 $D_t = F_t - F_{t+n}$ 作为编码器输入。这一“早期时序差分”（Td）机制通过元素级减法增强运动线索，同时增加 shortcut learning 的难度。可视化证据（Figure 2）清晰显示：朴素连续基线将提示视频中的背景噪声大量注入预测帧（红色矩形标注），而引入 Td 后背景噪声被有效抑制。

**3. 训练目标：引入时序对比学习（Tcl）**

仅靠 Td 虽能抑制背景噪声，但运动表征趋于稀疏，且随潜在维度增大，动作无关噪声会重新累积（Figure 3 中 S-PCFC 持续上升）。CoMo 进一步引入时序对比学习，通过构建正负运动对来强制潜在运动关注有意义的时序变化：

- **正对**：微小未来偏移的运动对 $Z_{t,t+n+\delta}$ 与 $Z_{t,t+n}$，相似度记为 $S_1$；
- **负对**：逆时序方向构造的运动对，包括 $Z_{t,t+n+\delta}$ 与 $Z_{t+n,t}$（相似度 $S_2$），以及 $Z_{t,t+n}$ 与 $Z_{t+n,t}$（相似度 $S_3$）。

InfoNCE 损失 $\mathcal{L}_{\mathrm{tcl}} = -\log \frac{e^{S_1}}{e^{S_1} + e^{S_2} + e^{S_3}}$ 最大化正对相似度、最小化负对相似度，使潜在运动聚焦于前景区域的细粒度动作变化。Figure 2 的橙色矩形标注显示，加入 Tcl 后预测的未来帧更准确地反映了从“未抓取”到“抓取”的细粒度动作转变。

### 协同机制与证据强度

Td 与 Tcl 的协同是 CoMo 有效性的核心。单独使用 Td 时，随潜在维度从 128 增至 512，S-PCFC 持续升高，表明动作无关噪声重新累积，MSE 在维度 512 时达到最高；而同时引入 Tcl 后，S-PCFC 始终保持低位，MSE 随维度增大持续下降（Figure 3）。这一协同效应最终转化为最强的下游策略性能：CoMo 在 LIBERO 四合一平均成功率达 80.1%，显著优于离散基线（75.9%）和朴素连续基线（75.2%），且 MSE（1.2588）和 S-PCFC（0.5496）均为最优（Table 1）。在 CALVIN 基准上，CoMo 将平均成功序列长度从 1.878 提升至 3.070（Table 2）。

**证据强度评估**：上述三项变更均有明确的消融实验支撑（Table 1, Figure 2, Figure 3），证据置信度达 0.95。跨形态泛化性在双机械臂和灵巧手等复杂肢体上也得到初步验证（Table 4），置信度 0.9，但需注意这些实验中绝对动作空间的 MSE 改善幅度相对有限，需结合更多平台进行交叉验证。

## 整体框架

CoMo 的整体框架建立在标准的逆动力学编码器—前向动力学解码器（IDM-FDM）范式之上，核心目标是从无动作标注的视频中学习**连续、无向量量化（VQ-free）的潜在运动表征**，并将其转化为伪动作标签，赋能机器人策略的联合训练。整个 pipeline 由两大阶段构成：**潜在运动学习阶段**和**统一策略联合训练阶段**。

### 潜在运动学习阶段

给定一对时间间隔为 $n$ 的帧 $(O_t, O_{t+n})$，CoMo 首先使用一个**共享权重的 MAE 预训练 ViT** 分别提取二者的 token 级特征 $F_t$ 和 $F_{t+n}$。随后，框架通过三个关键模块将视觉特征转化为连续潜在运动表征 $Z_{t,t+n}$：

1.  **早期时序差分（Td）**：对 $F_t$ 和 $F_{t+n}$ 执行逐元素相减，得到时序差分特征 $D_t = F_t - F_{t+n}$，同时**显式移除未来帧特征 $F_{t+n}$** 在编码器中的直接输入。这一设计从信息源头增加了 shortcut learning 的难度，迫使模型依赖运动线索而非静态背景。
2.  **Motion Qformer（Transformer）**：将当前帧特征 $F_t$、时序差分特征 $D_t$ 与一组可学习的查询向量拼接，通过标准的多层 Transformer 块进行交互，输出连续潜在运动表征 $Z$。由于去除了向量量化，$Z$ 的维度可以灵活扩展（如 128–512），保留了细粒度动态信息。
3.  **时序对比学习（Tcl）**：在潜在运动空间中引入 InfoNCE 损失，通过构造正负运动对来结构化表征。正对由微小未来偏移的帧对 $(Z_{t,t+n+\delta}, Z_{t,t+n})$ 构成，负对则通过直接反转时序方向构造 $(Z_{t,t+n+\delta}, Z_{t+n,t})$ 和 $(Z_{t,t+n}, Z_{t+n,t})$。该损失强制潜在运动聚焦于有意义的时序一致前景区域，抑制动作无关的背景噪声。

学得的潜在运动 $Z$ 随后送入**前向动力学解码器（FDM）**，以当前帧特征为条件重建未来帧，形成自监督训练闭环。整个 IDM-FDM 的训练损失由重建损失和时序对比损失联合构成。

### 统一策略联合训练阶段

在完成潜在运动编码器的训练后，CoMo 将其冻结并作为伪动作标签生成器。对于机器人数据集 $\mathcal{D}_R$（包含真实动作）和互联网视频数据集 $\mathcal{D}_V$（仅包含伪动作标签），框架在统一的生成式策略（扩散策略或自回归策略）中进行联合训练。具体而言，策略模型只需分配独立的轻量级输出头，分别预测机器人动作和视频潜在运动，即可实现数据层面的无缝混合。这种设计使得策略能够同时从稀缺的机器人示范和丰富的互联网视频中学习，显著提升数据效率——在 LIBERO 基准中仅使用 10 条机器人示教轨迹即可达到 80.1% 的平均成功率。

### Td 与 Tcl 的协同机制

Td 和 Tcl 在框架中并非孤立运作，而是形成互补的协同效应。消融实验（Figure 3）表明：单独使用 Td 虽能降低动作预测 MSE，但随着潜在运动维度增大，表征中的动作无关背景噪声持续增加（S-PCFC 指标上升）；引入 Tcl 后，S-PCFC 在各类维度下均保持低位，MSE 则持续下降。可视化结果（Figure 2）进一步印证了这一机制——Td 有效避免了朴素连续基线中的背景噪声污染，但运动表征较为稀疏；Tcl 的加入使运动更加聚焦于前景区域，预测的未来帧能准确反映从“未抓取”到“抓取”的细粒度动作变化。

### 补充图表

![[assets/figures/papers/paper_list_l848_https_arxiv_org_abs_2505_17006/figures/001_Figure_1.jpg]]
*Figure 1: The CoMo framework. (Left) CoMo model architecture. (Right) Temporal contrastive learning scheme. Built upon the standard IDM-FDM architecture, CoMo learn VQ-free, continuous and more precise inter-frame latent motion. CoMo introduces early temporal difference mechanism and temporal contrastive learning method to collaboratively ensure that the continuous latent motion focuses more on meaningful foreground regions and enhances action-relevant motion cues*

## 核心模块与公式推导

CoMo 围绕“逆动力学编码器–前向动力学解码器”（IDM–FDM）范式构建，核心目标是**无向量量化地学习连续潜在运动表征**，使其既保留细粒度动态信息，又与机器人动作空间保持一致的连续分布。为此，CoMo 引入两项关键设计：**早期时序差分机制（Td）** 和**时序对比学习（Tcl）**，二者协同作用以抑制 shortcut learning 并增强运动线索。

### 共享特征提取与早期时序差分

给定当前帧 $O_t$ 和未来帧 $O_{t+n}$，CoMo 使用一个**共享权重的 MAE 预训练 ViT** 分别提取 token 级特征 $F_t$ 和 $F_{t+n}$。与朴素连续基线直接编码 $[F_t, F_{t+n}]$ 不同，CoMo **显式移除未来帧特征**，转而计算时序差分特征：

$$D_t = F_t - F_{t+n}$$

这一早期时序差分操作（Td）在编码器输入端即增强运动线索，同时提高了模型依赖静态背景信息完成重建的难度，从而有效抑制 shortcut learning（Figure 2 红色框区域显示 Td 显著消除了背景噪声）。

![[assets/figures/papers/paper_list_l848_https_arxiv_org_abs_2505_17006/figures/002_Figure_2.jpg]]
*Figure 2: FDM future frame prediction visualization. Given sampled three frames from a prompt video, we extract latent motions from the first two and first to last frames, respectively. These motions are then used to predict the subsequent two frames via FDM in a new environment. The red rectangles indicate that the na¨ıve continuous baseline significantly incorporates static background noise from the prompt video. In contrast, the early temporal difference mechanism effectively avoids this issue. Crucially, as indicated by the orange rectangles, further introducing temporal contrastive learning leads to more precise latent motion representations. The results more accurately align with the fine-grain...*

### Motion Qformer 与连续潜在运动

将 $[F_t, D_t]$ 与一组可学习的查询向量（learnable query embeddings）拼接后，送入标准的 Transformer 块（Motion Qformer）进行交叉注意力交互，输出**连续潜在运动表征** $Z_{t,t+n}$。由于去除了 VQ-VAE 的向量量化约束，$Z_{t,t+n}$ 的维度可灵活扩展（如 128–512），无需受限于小码本（如 8 或 16）带来的信息瓶颈。

### 时序对比学习

仅靠 Td 虽能抑制背景噪声，但随潜在运动维度增大，动作无关噪声仍会重新渗入（Figure 3 中 S-PCFC 持续上升）。为此，CoMo 引入时序对比学习（Tcl），通过 InfoNCE 损失强制潜在运动关注有意义的时序变化：

![[assets/figures/papers/paper_list_l848_https_arxiv_org_abs_2505_17006/figures/003_Figure_3.jpg]]
*Figure 3: Scalability of latent motion dimension in Libero. As the latent motion dimension increases, relying solely on the temporal difference mechanism leads to a persistent increase of actionirrelevant background noise (indicated by an increasing S-PCFC). This impairs regression performance, resulting in the highest MSE at a dimension of 512. In contrast, further incorporating temporal contrastive learning (our CoMo) effectively addresses this issue and ensures the scalability of the latent motion dimension*

$$\mathcal{L}_{\mathrm{tcl}} = -\log \frac{e^{S_1}}{e^{S_1} + e^{S_2} + e^{S_3}}$$

其中三项余弦相似度定义如下：

- **正对相似度** $S_1 = S(Z_{t,t+n+\delta}, Z_{t,t+n})$：对同一视频，以微小未来偏移 $\delta$ 构造正运动对，二者应具有高度语义一致性。
- **负对相似度** $S_2 = S(Z_{t,t+n+\delta}, Z_{t+n,t})$：逆时序方向构造的负运动对，迫使模型排斥时间反转的错误配对。
- **负对相似度** $S_3 = S(Z_{t,t+n}, Z_{t+n,t})$：另一逆时序方向的负对，进一步增强时序判别力。

Tcl 的核心机制在于：正对共享相似的“未来变化模式”，而负对则呈现相反的时序方向。通过最大化 $S_1$ 并最小化 $S_2$、$S_3$，潜在运动被迫聚焦于前景区域的真实运动变化，而非静态背景或无关噪声（Figure 2 橙色框区域显示 Tcl 使运动预测更精确地对应从“未抓取”到“抓取”的细粒度动作变化）。

### 前向动力学解码器与联合训练

前向动力学解码器（FDM）以当前帧特征 $F_t$ 和潜在运动 $Z_{t,t+n}$ 为条件，重建未来帧 $\hat{O}_{t+n}$。FDM 的重建损失与 Tcl 损失共同优化 IDM 编码器，使学得的连续潜在运动既能准确预测未来视觉状态，又具有结构化的时序判别能力。

在下游策略联合训练阶段，CoMo 将视频数据集 $\mathcal{D}_V$ 中的潜在运动作为**伪动作标签**，与机器人数据集 $\mathcal{D}_R$ 的真实动作标签合并，在统一生成式策略（扩散策略或自回归策略）中进行联合模仿学习。策略网络仅需为两类数据分配独立的轻量预测头，即可无缝利用互联网视频中的运动先验。

## 实验与分析

### 核心发现：连续潜在运动与联合训练的有效性

CoMo在多个基准上验证了其核心主张：去除向量量化并引入早期时序差分（Td）与时序对比学习（Tcl）协同作用，能够从无动作互联网视频中学习高质量的连续潜在运动，并作为伪动作标签赋能统一策略的联合训练。

在**LIBERO**基准上，CoMo在极度数据受限条件下（每任务仅10条机器人示范，远低于常规的50条）取得平均成功率**80.1%**，显著优于不使用视频的扩散策略基线DP（w/o videos）的**70.4%**（Table 3），提升**+9.7个百分点**。这表明联合训练机制能够有效利用视频数据中的运动先验，弥补机器人示范稀缺带来的性能缺口。

![[assets/figures/papers/paper_list_l848_https_arxiv_org_abs_2505_17006/figures/006_Table_3.jpg]]
*Table 3: Comparison results with other related methods on the LIBERO benchmark. Similarly, only 10 robot action demonstrations per task are used*

在**CALVIN**长序列操作基准（ABC→D）上，CoMo将平均成功序列长度从无运动基线的**1.878**提升至**3.070**（Table 2），提升**+1.192**。这验证了连续潜在运动在需要长时程推理的自回归策略范式下同样有效。

![[assets/figures/papers/paper_list_l848_https_arxiv_org_abs_2505_17006/figures/005_Table_2.jpg]]
*Table 2: Experiment results on CALVIN. ×4 indicates that we expand the latent motion dimension from 128 to 512*

### 消融实验：Td与Tcl的协同机制

Table 1的系统消融揭示了各组件对运动质量和策略性能的因果贡献：

**离散化 vs. 连续化**：离散潜在运动基线（Dis.）虽然通过向量量化部分缓解了shortcut learning，但引入严重信息损失——其动作预测MSE高达**5.6743**，远高于CoMo的**1.2588**；同时离散码本与连续动作空间的分布不一致导致策略成功率仅为**75.9%**，低于CoMo的**80.1%**。朴素连续基线（Con.）虽保留信息完整性（MSE **1.6256**），但S-PCFC指标高达**0.9268**，表明潜在运动中混杂大量动作无关背景噪声，策略成功率仅**75.2%**。

**Td的独立效应**：引入早期时序差分后（Con.+Td），S-PCFC降至**0.4810**，MSE降至**1.2742**，策略成功率提升至**78.2%**。Figure 2的可视化证实，Td有效抑制了背景噪声（红色矩形区域），但运动表征趋于稀疏。

**Tcl的补充效应**：进一步引入时序对比学习（Con.+Td+Tcl，即CoMo）后，S-PCFC进一步降至**0.5496**，MSE降至**1.2588**，策略成功率提升至**80.1%**。Figure 2的橙色矩形区域显示，Tcl使运动表征更聚焦前景、更结构化，预测的未来帧更准确地反映从“未抓取”到“抓取”的细粒度动作变化。

**维度可扩展性**：Figure 3揭示了Td与Tcl在潜在运动维度扩展时的协同必要性。当仅使用Td时，随着维度从128增至512，S-PCFC持续升高，表明动作无关噪声随容量增大而累积，MSE在512维时达到最高；而CoMo（Td+Tcl）在全部维度范围内保持S-PCFC低位稳定，MSE持续下降，证明Tcl有效抑制了高维空间中的shortcut learning复发。

### 跨形态泛化与真实世界验证

CoMo在复杂机器人形态上同样展现优势。Table 4显示，在双机械臂（Dual-arm）和灵巧手（Humanoid）等具有高维绝对动作空间的形态上，CoMo的Td和Tcl组合持续降低动作预测MSE（双机械臂：**4.9665** vs. 连续基线**5.2916**；灵巧手：**0.0732** vs. **0.0783**），验证了方法的跨形态泛化性。

在真实世界Franka机械臂实验中（Table 5），CoMo在多个操作任务上取得可靠成功率，进一步证明了从互联网视频学得的连续潜在运动能够零样本迁移至物理机器人场景。

![[assets/figures/papers/paper_list_l848_https_arxiv_org_abs_2505_17006/figures/008_Table_5.jpg]]
*Table 5: Real-world experiment results on Franka robot arm*

### 局限性分析

尽管整体有效，CoMo在部分任务上的增益有限——例如LIBERO-Long上仅从**53.7%**提升至**62.0%**（Table 1），提示长序列任务中伪动作标签的质量或联合训练策略仍有改进空间。当前CoMo依赖固定帧对输入，尚未扩展到多帧、多视角建模，可能无法有效应对遮挡和复杂动态场景。此外，伪动作标签质量高度依赖CoMo在领域外的泛化能力，当源域与目标域差距过大时性能可能下降，这一点需在实际部署中手动验证。

![[assets/figures/papers/paper_list_l848_https_arxiv_org_abs_2505_17006/figures/004_Table_1.jpg]]
*Table 1: Ablation results on the LIBERO benchmark. Notably, our results are achieved under a severe data constraint, utilizing only 10 action-annotated robot demonstrations per task, a significant reduction compared to the 50 used in typical settings*

### 补充图表

![[assets/figures/papers/paper_list_l848_https_arxiv_org_abs_2505_17006/figures/009_Table_4.jpg]]
*Table 4: Ablation results of action prediction MSE in absolute action space of more complex embodiments*

![[assets/figures/papers/paper_list_l848_https_arxiv_org_abs_2505_17006/figures/007_Figure_4.jpg]]
*Figure 4: Real-world task illustrations*

![[assets/figures/papers/paper_list_l848_https_arxiv_org_abs_2505_17006/figures/010_Figure_5.jpg]]
*Figure 5: The real-world Franka robot arm experiments hardware platform*

![[assets/figures/papers/paper_list_l848_https_arxiv_org_abs_2505_17006/figures/011_Figure_6.jpg]]
*Figure 6: The FDM future frame prediction visualization*

![[assets/figures/papers/paper_list_l848_https_arxiv_org_abs_2505_17006/figures/012_Table_6.jpg]]
*Table 6: The training and architectural hyperparameters for our CoMo learning*

## 方法谱系与知识库定位

### 问题定位：从离散到连续的潜在运动学习

CoMo 处于“从无动作标注的视频中自监督学习运动表征以赋能机器人策略”这一研究脉络的核心。该脉络的**核心瓶颈**在于：无监督地从无动作视频中学习帧间潜在运动时，模型极易陷入 **shortcut learning**——倾向于捕获静态背景信息而非前景运动，导致潜在运动包含大量动作无关噪声，无法提供有效的伪动作标签。

该脉络中存在两条主要技术路线：

**离散潜在运动路线**：以 **GR00T** 和 **Moto**（Chen et al., ICCV 2025）为代表，采用 VQ-VAE 向量量化将潜在运动约束到小码本（如 8 或 16 个离散编码），通过信息瓶颈强制模型关注运动信息。该路线的**优势**在于能有效抑制 shortcut learning，但**代价**是信息损失严重——Table 1 中 Dis. 变体的动作预测 MSE 高达 5.6743，远高于 CoMo 的 1.2588，且离散表征与机器人连续动作空间分布不一致，限制了策略性能（成功率 75.9% vs 80.1%）。

**连续潜在运动路线**：朴素连续基线（Con.）去除向量量化以保留完整信息，但缺乏对 shortcut 的有效抑制，导致 S-PCFC 指标高达 0.9268（Table 1），表明潜在运动中混杂大量动作无关背景噪声。**Dynamo**（Cui et al., NeurIPS 2024）尝试通过协方差正则化抑制 shortcut，但在该论文的对比中未作为主要基线出现。

### CoMo 的方法定位与创新

CoMo 在连续潜在运动路线上做出了**两项协同创新**，在不牺牲信息完整性的前提下有效缓解 shortcut learning：

1. **早期时序差分机制（Td）**：在逆动力学编码器输入端，显式移除未来帧特征 $F_{t+n}$，仅使用当前帧特征 $F_t$ 和时序差分特征 $D_t = F_t - F_{t+n}$。这一设计从信息源头上增加 shortcut 难度，同时增强运动线索。Figure 2 的可视化表明，仅 Td 即可消除朴素连续基线中的背景噪声（红色框区域）。

2. **时序对比学习（Tcl）**：通过 InfoNCE 损失构建正负运动对的结构化表征。正对由微小未来偏移的帧对构成（$S_1 = S(Z_{t,t+n+\delta}, Z_{t,t+n})$），负对通过直接反转时序方向构造（$S_2$ 和 $S_3$）。该损失强制潜在运动关注与后续帧一致的有意义前景区域，使运动表征更聚焦、更结构化（Figure 2 橙色框区域）。

**二者协同的必要性**在 Figure 3 中得到充分验证：单独使用 Td 时，随着潜在运动维度增大（128→512），S-PCFC 持续升高，表明背景噪声重新渗入；只有结合 Tcl 后，S-PCFC 才保持低位，MSE 持续下降，最终策略成功率最优。这说明 Td 提供“防御性”噪声抑制，Tcl 提供“建设性”运动结构化，二者缺一不可。

### 与其他预测信号方法的对比

在利用视频预测信号辅助机器人策略的谱系中，CoMo 与以下方法形成对比：

- **ATM**（Wen et al., RSS 2024）：基于任意点轨迹建模，直接预测像素级运动轨迹作为辅助信号。CoMo 与之不同，在紧凑的潜在空间中学习运动表征，避免了像素空间的高维噪声和计算开销。
- **GR2-like**：使用未来帧视觉特征作为辅助信号。该方法本质上是 CoMo 消融中的“Future features”变体——直接使用 MAE ViT 的未来帧特征作为潜在运动。Table 1 显示该方法 S-PCFC 极高（0.9268），验证了未经 Td 和 Tcl 处理的原始视觉特征包含大量动作无关信息。

### 适用边界与局限

CoMo 在以下条件下表现出色，但也存在明确的适用边界：

**已验证的有效范围**：
- **数据效率场景**：LIBERO 实验仅使用 10 条机器人示范轨迹（典型设置 50 条），CoMo 将成功率从 70.4% 提升至 80.1%（Table 3），证明其在极端数据稀缺下的价值。
- **跨策略范式**：在扩散策略（LIBERO）和自回归策略（CALVIN）上均有效，CALVIN 平均完成跨度从 1.878 提升至 3.070（Table 2）。
- **跨形态迁移**：在双机械臂和灵巧手等复杂形态上，Td+Tcl 进一步降低绝对动作空间的 MSE（Table 4），表明方法具有跨形态泛化性。

**已知局限**：
- **长时序任务增益有限**：在 LIBERO-Long 上，成功率仅从 53.7% 提升至 62.0%（Table 1），表明 CoMo 对需要长程依赖的任务帮助有限，可能受限于固定帧对输入的设计。
- **遮挡与复杂动态**：当前 CoMo 依赖固定帧对输入，尚未扩展到多帧、多视角建模，可能无法有效处理遮挡和复杂动态场景。
- **域外泛化依赖**：伪动作标签的质量高度依赖 CoMo 在领域外的泛化能力。当源域（互联网视频）与目标域（特定机器人平台）差距过大时，性能可能下降。论文使用 SAM-V、EgoVid、Droid 各 40,000 个视频训练，覆盖了较广的视觉域，但该泛化边界仍需进一步刻画。

### 开放问题

1. **规模化极限**：CoMo 在 120,000 个互联网视频上训练，但能否通过更大规模、更复杂的真实世界精细操作视频进一步释放潜力，仍是一个开放问题。

2. **多帧多视角扩展**：能否将 CoMo 的 Td+Tcl 范式扩展到多帧、多视角的潜在运动建模，以缓解遮挡并捕捉更长时程的时序依赖？

3. **评估指标的鲁棒性**：MSE 和 S-PCFC 的组合指标在 LIBERO 上与策略成功率高度相关，但这种相关性是否在不同任务和机器人平台上保持鲁棒，尚需更多验证。

4. **联合训练的负迁移风险**：在大规模异构机器人数据下，统一连续策略的联合训练是否会遭遇负迁移？如何自动平衡机器人动作数据和视频伪标签数据的贡献权重？

## 原文 PDF

![[paperPDFs/CVPR_2026/CoMo_Learning_Continuous_Latent_Motion_from_Internet_Videos_for_Scalable_Robot_Learning.pdf]]

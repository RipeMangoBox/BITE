---
title: "Towards Motion Turing Test: Evaluating Human-Likeness in Humanoid Robots"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Towards_Motion_Turing_Test_Evaluating_Human_Likeness_in_Humanoid_Robots.pdf
project_link: null
code_link: "https://huggingface.co/datasets/lvhaidong/LAFAN1_Retargeting_Dataset"
aliases:
- PNPTRN
- TMTTEHLHR
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 引入 Motion Turing Test 评估范式，将运动评估统一到纯运动学的 SMPL-X 表示，完全消除外观干扰，并将类人性判断形式化为基于时序图卷积网络（PTR-Net）的回归任务，直接从运动序列预测 0-5 分数。
primary_logic: 人类对运动类人性的感知主要由姿态、节奏、协调性等运动学特征决定，该感知可通过数据驱动的时序回归模型有效建模；在运动图灵测试基准上，简单的 PTR-Net 显著优于大型多模态模型。
claims:
- 人类与机器人动作之间存在显著的类人性评分差异，跳跃等动态类别差异达 3.23 分（0-5 量表）。
- PTR-Net 在 Motion Turing Test 上取得 MAE 0.5813、Spearman's ρ 0.6841，远超 Gemini 2.5 Pro（MAE 1.2682, ρ 0.2303）。
- 移除时间编码器后 MAE 升至 0.7631，验证了时序建模的关键作用。
- 在分布外 XPeng IRON 机器人上，PTR-Net 预测分数 4.25 与人类评分 4.36 高度吻合。
---

# Towards Motion Turing Test: Evaluating Human-Likeness in Humanoid Robots

> [!tip] 核心洞察
> 人类对运动类人性的感知主要由姿态、节奏、协调性等运动学特征决定，该感知可通过数据驱动的时序回归模型有效建模；在运动图灵测试基准上，简单的 PTR-Net 显著优于大型多模态模型。

| 字段 | 内容 |
|------|------|
| 中文题名 | 迈向运动图灵测试：评估人形机器人运动的类人性 |
| 英文题名 | Towards Motion Turing Test: Evaluating Human-Likeness in Humanoid Robots |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2603.06181) · [HuggingFace](https://huggingface.co/datasets/lvhaidong/LAFAN1_Retargeting_Dataset) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | PTR-Net (Pose-Temporal Regression Network) |
| Dataset | Motion Turing Test |

> [!tip] 效果简介
> - Motion Turing Test (HHMotion) 上，MAE ↓ 0.5813 vs 1.2682 (Gemini 2.5 Pro PA-CoT) (-0.6869)；Spearman's ρ ↑ 0.6841 vs 0.2303 (Gemini 2.5 Pro PA-CoT) (+0.4538)；MAE ↓ 0.5813 vs 0.6252 (MotionBERT Fine-tuned) (-0.0439)。

## 概要

人形机器人正从实验室走向现实场景，但其运动表现是否真正“类人”仍缺乏客观、标准化的评估手段。现有评估多依赖外观、任务成功率或主观印象，难以剥离运动本身的质素。本文受图灵测试启发，提出**运动图灵测试（Motion Turing Test）** 范式：将评估统一到纯运动学的 SMPL-X 骨架表示，完全消除外观干扰，让评估聚焦于姿态、节奏与协调性等运动学特征。

核心发现是，人类观察者仅凭运动学数据即可可靠地区分机器人与人类动作，尤其在跳跃、拳击、跑步等高频动态类别中，类人性评分差异可达 3.23 分（0–5 量表）。更重要的是，这一感知可通过数据驱动的时序回归模型有效建模——本文提出的 **PTR-Net（Pose-Temporal Regression Network）** 在基准上取得 MAE 0.5813、Spearman’s ρ 0.6841，显著优于 Gemini 2.5 Pro 等大型多模态模型（MAE 1.2682, ρ 0.2303），验证了专用时序建模在此任务中的关键作用。

为支撑这一评估范式，作者构建了 **HHMotion（Human-Humanoid Motion）数据集**，包含 1000 条运动序列、15 个动作类别，覆盖 11 种机器人模型与 10 名人类被试，并投入 30 名标注者、超 500 小时人工评分。该基准为类人运动生成与控制方法提供了首个标准化测试平台，相关代码与数据集已开源。



### 人形机器人运动的类人性评估困境

人形机器人正从实验室走向家庭服务、工业协作等真实场景，其运动的自然度和类人性直接影响用户接受度和人机交互体验。然而，当前领域面临一个核心瓶颈：尽管许多机器人动作在表面观感上已相当流畅，人类观察者仍能轻易辨别其与真实人类动作的差异，尤其在跳跃、拳击、跑步等高频动态动作中，这种差异尤为显著——根据本研究构建的基准，跳跃类动作的人-机器人评分差异可达 **3.23 分**（0–5 量表，见 Table 2）。

这一困境的根源在于，现有的运动评估方法存在两个结构性缺口：

1. **缺乏统一的标准化评估基准**：传统评估依赖特定任务的指标（如轨迹误差、成功率）或主观的视觉观察，缺少专门针对“类人性”这一维度的客观、可复现的量化标准，导致不同方法之间难以公平比较，也使得运动生成方法的优化方向模糊不清。

2. **外观与运动的耦合干扰**：直接观看机器人视频时，评估者不可避免地受到机器人外观（机械结构、外壳材质等）的影响，难以将注意力纯粹聚焦于运动本身的质量——即姿态、节奏、协调性等运动学特征。这种耦合使得“类人性”评估的信度受到外观偏差的污染。

### 核心动机：建立纯运动学的类人性测试范式

针对上述缺口，本文的核心动机是提出**运动图灵测试（Motion Turing Test）**：借鉴图灵测试的思想，将评估问题转化为“仅凭运动学数据，人类观察者能否区分机器人与人类的动作”。具体而言，所有视频中的动作被统一转换为 **SMPL-X** 骨架表示，彻底剥离外观信息，使评估者仅依赖关节运动序列做出判断（见 Figure 1）。

这一范式转换带来了两个关键优势：
- **消除外观偏差**：所有动作在统一的骨架表示下比较，确保评估聚焦于运动本身。
- **量化可复现**：通过招募 30 名标注者对 1,000 段运动序列进行 0–5 的类人性评分（累计超过 500 标注小时），构建了 **HHMotion（Human-Humanoid Motion）数据集**，为后续自动化评估模型的训练和测试提供了标准化基准。

### 从人工评估到自动化评估的动机

人工评估虽然可靠，但成本高昂且难以规模化。因此，本文进一步探索**自动化类人性评估模型**的可行性，将其形式化为一个从运动序列到标量分数的回归任务。这一设计背后的核心洞察是：人类对运动类人性的感知主要由运动学特征决定，这种感知可以通过数据驱动的时序回归模型有效建模。初步实验表明，一个结构简单的 **PTR-Net（Pose-Temporal Regression Network）** 即可在该任务上显著超越 Gemini 2.5 Pro 等大型多模态模型（MAE 0.5813 vs. 1.2682，Spearman's ρ 0.6841 vs. 0.2303，见 Table 3），验证了专用运动理解模型在该场景下的必要性。

综上，本文的动机链条可概括为：**识别类人性评估的标准化缺失 → 提出纯运动学的运动图灵测试范式 → 构建标注基准 → 探索自动化回归模型**，为人形机器人运动生成与控制的研究提供一个可量化、可复现的评估锚点。



## 核心方法与创新机理

本工作的核心创新在于将人形机器人运动类人性评估从定性、主观的视觉判断，重构为一个**统一的、可量化的回归任务**，并为此构建了完整的评估基准与基线模型。具体而言，创新体现在三个层面：

### 1. 评估范式的根本转变：运动图灵测试

传统人形机器人运动评估受外观、环境、任务上下文等多重因素干扰，难以分离出运动本身的类人性。本工作提出**运动图灵测试（Motion Turing Test）**，将评估统一到纯运动学的 **SMPL-X 骨架表示**，完全消除外观线索，使评估者仅基于姿态序列的运动学特征（姿态、节奏、协调性）判断类人性。这一范式转移的关键因果机制在于：将类人性判断从多模态感知问题降维为纯时序运动学回归问题，从而使得自动化评估成为可能。

### 2. 核心方法：PTR-Net 的四个关键设计变更

基于上述范式，作者提出 **PTR-Net (Pose-Temporal Regression Network)**，将类人性评估形式化为从运动序列 $\mathbf{X}$ 到标量分数 $s \in [0,5]$ 的端到端映射 $s = f_{\theta}(\mathbf{X})$。相较于 VLM-based 方法（如 Gemini 2.5 Pro、GPT-4o）和传统动作识别模型（如 MotionBERT），PTR-Net 在以下四个关键设计槽位上做出了针对性改进：

| 设计槽位 | 基线方法 | PTR-Net 设计 | 证据强度 |
|----------|---------|-------------|---------|
| **时序建模** | 忽略帧间关系（各帧独立或平均池化） | 双层双向 LSTM，捕捉长程时序依赖 | 强（移除后 MAE 从 0.5813 升至 0.7631，Table 4） |
| **空间图邻接** | 可学习邻接矩阵或无图结构（MLP） | 无参数邻接矩阵（parameter-free adjacency），自适应聚合骨架空间关系 | 中（消融验证优于常规 GCN 和 MLP，Table 4） |
| **时序特征聚合** | 平均池化或无池化 | 注意力加权池化（Attention Pooling），自适应选择关键帧 | 中（Table 4 消融验证） |
| **训练目标** | 单纯 L2 回归损失 | L2 回归损失 + 时序平滑正则化 $\mathcal{L}_{\mathrm{reg}}$，抑制预测分数剧烈波动 | 中（Table 4 消融验证） |

训练损失函数为：
$$\mathcal{L} = \|\hat{s} - s^{*}\|_{2}^{2} + \lambda \mathcal{L}_{\mathrm{reg}}$$

其中 $\mathcal{L}_{\mathrm{reg}}$ 惩罚相邻帧预测分数的大幅跳变，确保时序一致性。

### 3. 创新效果的决定性证据

在 Motion Turing Test 基准上，PTR-Net 的 **MAE 为 0.5813，Spearman's ρ 为 0.6841**，远超最优 VLM 方法 Gemini 2.5 Pro (PA-CoT) 的 MAE 1.2682 和 ρ 0.2303（Table 3）。这一显著差距揭示了当前大型多模态模型在纯运动学理解上的根本局限——它们擅长视觉-语言对齐，却难以捕捉姿态序列中细微的类人性差异。

消融实验进一步验证了各设计组件的贡献：**移除时间编码器后 MAE 升至 0.7631**，证实时序建模是模型性能的核心支柱（Table 4）。此外，在分布外机器人 **XPeng IRON** 上，PTR-Net 预测分数 4.25 与人类评分 4.36 高度吻合（Figure 10），初步验证了模型的泛化能力。

### 4. 局限与开放问题

尽管 PTR-Net 在运动学层面有效建模了类人性，但其设计存在固有局限：（1）仅依赖 SMPL-X 骨架运动学，无法捕获肌肉动力学、接触力等更精细的类人特征；（2）模型在更广泛的新形态机器人上的分布外鲁棒性尚未充分验证；（3）当前评估未融合意图性、适应性、任务完成度等高层次类人性维度。这些局限指向了未来工作的关键方向：如何让自动评估模型超越运动学特征，形成更全面的类人性评估体系。



该工作围绕**运动图灵测试（Motion Turing Test）** 构建了一套从数据采集、表示标准化、人工标注到自动评估的完整流水线。其核心设计动机是消除外观线索的干扰，将类人性判断严格限定在运动学层面。

### 统一表示与评估范式

流水线的入口是多样化的运动视频源，包括真实人形机器人、仿真环境、人类被试、人类模仿机器人以及 YouTube 公开视频。所有视频统一通过 **GVHMR** 进行姿态估计，转换为 **SMPL-X** 骨架表示。这一步是关键瓶颈的解决方案：SMPL-X 仅保留关节旋转与位置的时序运动学信息，完全剥离了机器人外观、材质、背景等与运动无关的视觉特征，使得后续评估聚焦于姿态、节奏与协调性本身。

评估任务被形式化为一个**标量回归问题**：给定一段 SMPL-X 运动序列 $\mathbf{X} \in \mathbb{R}^{T \times J \times D}$（$T$ 为帧数，$J$ 为关节点数，$D$ 为特征维度），模型需输出一个连续的类人性分数 $s \in [0, 5]$。人工标注端采用相同的 0–5 Likert 量表，由 25 名高一致性标注者完成评分，为自动评估提供监督信号。

### 自动评估模型 PTR-Net

为了从纯运动学序列中提取类人性特征，作者提出了 **PTR-Net (Pose-Temporal Regression Network)** 作为基准模型。其架构由四个模块串联构成：

1. **Temporal Encoder（时间编码器）**：双层双向 LSTM，负责捕捉长程时序依赖，将原始姿态序列编码为时间感知的特征表示。消融实验表明，移除该模块后 MAE 从 0.5813 升至 0.7631（Table 4），验证了时序建模对类人性感知的核心作用。
2. **Spatial-Temporal Graph Convolution（时空图卷积）**：采用无参数邻接矩阵的 ST-GCN，自适应地聚合骨架图上的空间-时间关系，避免了对预定义邻接结构的依赖。
3. **Attention Pooling（注意力池化）**：通过注意力机制对不同时间步的特征进行加权聚合，生成定长的运动表征，使模型能够聚焦于对类人性判断最关键的帧段。
4. **Score Regressor（分数回归器）**：全连接层将聚合特征映射为标量分数。

训练目标为 L2 回归损失与时序平滑正则化 $\mathcal{L}_{\mathrm{reg}}$ 的组合：
$$\mathcal{L} = \|\hat{s} - s^{*}\|_{2}^{2} + \lambda \mathcal{L}_{\mathrm{reg}}$$
其中正则项抑制预测分数在相邻帧间的剧烈波动，提升时序一致性。

### 输入-输出流

整体数据流可概括为：**多源视频 → GVHMR 姿态估计 → SMPL-X 骨架序列 → 人工标注（0–5 分）→ PTR-Net 训练/推理 → 类人性分数输出**。推理阶段，PTR-Net 直接以 SMPL-X 序列为输入，端到端输出 $s = f_{\theta}(\mathbf{X})$，无需任何外观或上下文信息。

图 3 展示了该流水线的完整概览：从机器人/人类视频采集开始，经 SMPL-X 转换后送入人工评分流程，最终产出量化的类人性评估结果。这一设计确保了评估标准的统一性和可复现性，为运动生成方法的优化提供了客观基准。

### 补充图表

![[assets/figures/papers/paper_list_l1045_https_arxiv_org_abs_2603_06181/figures/001_Figure_1.jpg]]
*Figure 1: Motion Turing Test: Evaluators judge whether the pose sequence resembles human motion, focusing solely on motion without appearance cues*

![[assets/figures/papers/paper_list_l1045_https_arxiv_org_abs_2603_06181/figures/004_Figure_3.jpg]]
*Figure 3: Overview of the human scoring pipeline, where all the humanoid robot and human motions are converted into SMPL-X poses and evaluated by human annotators. The resulting 0–5 scores quantitatively assess the human-likeness of each motion*



PTR-Net 将类人性评估形式化为一个端到端的回归任务：给定一段运动序列 $\mathbf{X} \in \mathbb{R}^{T \times J \times C}$（$T$ 帧，$J$ 个关节，$C$ 维特征），模型学习映射函数 $s = f_{\theta}(\mathbf{X})$，输出标量分数 $s \in [0, 5]$。该方法的核心在于通过时序编码、空间-时间图卷积与注意力聚合三个模块，从纯运动学数据中提取判别性特征。

### 时序编码器

运动类人性的判别高度依赖帧间依赖关系——例如，跳跃动作的起跳、腾空、落地构成一个不可分割的时序整体。PTR-Net 采用双层双向 LSTM 作为时序编码器，对输入的 SMPL-X 姿态序列进行逐帧编码，输出时序增强的特征 $\mathbf{H}_t \in \mathbb{R}^{2h}$。消融实验（Table 4）提供了决定性证据：移除该模块后，MAE 从 0.5813 升至 0.7631，RMSE 从 0.7926 升至 0.9691，验证了长程时序建模对评估精度的关键作用。

### 空间-时间图卷积

在时序编码之后，模型通过空间-时间图卷积网络对骨架拓扑关系进行建模。与常规 GCN 使用可学习邻接矩阵不同，PTR-Net 采用无参数邻接矩阵，使图结构自适应地聚合空间特征，避免了人工定义关节连接关系带来的归纳偏置。消融研究表明，该设计优于 MLP 和常规 GCN 变体，验证了自适应空间特征聚合的有效性。

### 注意力池化与分数回归

为将变长时序特征压缩为定长表示，PTR-Net 引入注意力加权池化机制：模型自动学习不同时间步的重要性权重，对关键帧（如动作转折点）赋予更高关注度，而非简单地进行平均池化。聚合后的特征通过全连接层映射为最终的类人性分数。

### 训练目标

训练损失函数由两部分组成：

$$\mathcal{L} = \|\hat{s} - s^{*}\|_{2}^{2} + \lambda \mathcal{L}_{\mathrm{reg}}$$

其中 $\hat{s}$ 为预测分数，$s^{*}$ 为人类标注的真实分数。第一项为标准 L2 回归损失，驱动预测值逼近人类判断；第二项 $\mathcal{L}_{\mathrm{reg}}$ 为时序平滑正则项，惩罚相邻帧间预测分数的剧烈波动，从而提升评估的时序一致性。消融实验表明，全模型（含注意力池化与平滑正则）在误差降低与排序一致性之间达到了最优平衡。

### 补充图表

![[assets/figures/papers/paper_list_l1045_https_arxiv_org_abs_2603_06181/figures/008_Figure_7.jpg]]
*Figure 7: Our proposed PTR-Net baseline consists of a temporal encoder, spatial-temporal graph convolution, and attention pooling, then uses a score regressor to predict the human-likeness score*

![[assets/figures/papers/paper_list_l1045_https_arxiv_org_abs_2603_06181/figures/005_Figure_4.jpg]]
*Figure 4: Human-likeness scoring rules used in evaluating motion clips on a 0–5 Likert scale, focusing solely on motion quality*



## 实验与关键发现

### 运动图灵测试基准的定量结果

我们在构建的 HHMotion 基准上对各类评估方法进行了系统比较。核心指标包括平均绝对误差（MAE）、均方根误差（RMSE）和斯皮尔曼等级相关系数（ρ），分别衡量预测分数与人类标注分数的绝对偏差、大误差惩罚和排序一致性。

**PTR-Net 显著优于基于大视觉语言模型（VLM）的方法。** 如 Table 3 所示，PTR-Net 取得 MAE 0.5813、RMSE 0.7926、Spearman's ρ 0.6841 的最佳综合表现。相比之下，表现最好的 VLM 方法 Gemini 2.5 Pro（PA-CoT，即逐步推理提示策略）的 MAE 高达 1.2682，RMSE 为 1.5214，而 ρ 仅为 0.2303，说明其预测分数与人类判断的排序一致性极弱。GPT-4o 的表现更差，MAE 为 1.3224，ρ 仅 0.1482。部分 VLM（如 Qwen3-VL-Plus）在不同提示策略下输出恒定值，导致 ρ 无效（Table 3 中以“–”标记），暴露出通用多模态模型在理解纯骨架运动序列方面的根本性困难。

**PTR-Net 亦优于微调后的预训练动作识别模型。** MotionBERT（Zhu et al., ICCV 2023）在 HHMotion 上微调后取得 MAE 0.6252、ρ 0.6366，虽明显优于 VLM 方法，但仍落后 PTR-Net 约 7.5% 的 MAE 和 4.8 个百分点的 ρ。这表明，即便具备骨架动作理解能力的预训练模型，在类人性回归这一特定任务上仍不及专门设计的时序回归架构。

**时序建模是类人性评估的关键瓶颈。** 消融实验（Table 4）显示，移除时间编码器后 MAE 从 0.5813 急剧升至 0.7631，RMSE 从 0.7926 升至 0.9691，降幅超过 30%。这证实了类人性判断高度依赖于帧间的运动节奏、过渡平滑性和协调性等时序特征，而非单帧姿态的静态分析。

### 组件消融与设计验证

我们通过逐步移除或替换 PTR-Net 各组件，验证了架构设计的合理性。

- **空间图卷积的有效性：** 将无参数邻接矩阵的 ST-GCN 替换为常规 GCN 或 MLP 后，MAE 分别升至 0.6218 和 0.6473（Table 4）。无参数邻接矩阵允许模型自适应学习骨架关节点之间的空间依赖关系，避免了人工预定义拓扑或可学习参数带来的过拟合风险。
- **注意力池化的贡献：** 将注意力加权池化替换为平均池化后，MAE 升至 0.6103，ρ 降至 0.6542。注意力机制使模型能够动态聚焦于对类人性判断最关键的时间片段（如动作转折点或失衡瞬间），而非对所有帧等权处理。
- **时序平滑正则化的作用：** 去除正则项 $\mathcal{L}_{\mathrm{reg}}$ 后，MAE 升至 0.6089，且预测分数的时序波动增大。该正则项通过惩罚相邻帧预测分数的剧烈跳变，确保了评估结果的时序一致性，与人类感知的连续性相吻合。

![[assets/figures/papers/paper_list_l1045_https_arxiv_org_abs_2603_06181/figures/013_Table_4.jpg]]
*Table 4: Ablation study of PTR-Net components on the Motion Turing Test benchmark*

全模型在误差降低和排序一致性之间达到最优平衡，验证了各组件协同设计的合理性。

### 动作类别的类人性差异分析

Table 2 按人类与真实人形机器人之间的类人性评分差异对动作类别进行排序，揭示了当前机器人运动能力的优势与短板。

![[assets/figures/papers/paper_list_l1045_https_arxiv_org_abs_2603_06181/figures/007_Table_2.jpg]]
*Table 2: Top 5 and bottom 5 action categories ranked by score difference between human and real humanoid motions. The scores here are calculated based on the average score of the last 25 annotators after the IAC check*

**差异最小的类别（机器人表现接近人类）：** 挥手（waving）、舞蹈（dance）、行走（walk）等周期性或低动态动作的评分差异较小。例如，挥手动作中人类平均分与机器人平均分的差距仅约 0.5 分（0–5 量表），说明机器人在执行规律性上肢动作时已能达到较高的类人程度。

**差异最大的类别（机器人表现远逊人类）：** 跳跃（jumping）、拳击（boxing）、跑步（running）等高频动态动作的评分差异最大，跳跃动作的差异高达 3.23 分。如 Figure 6 所示，机器人在这些动作中常出现关节角度突变、重心不稳和肢体协调性差等问题，SMPL-X 骨架序列清晰反映了这些运动学层面的不自然特征。这为运动生成和控制器优化提供了明确的方向：优先改善高动态动作的时序平滑性和物理合理性。

### 分布外泛化验证

为检验 PTR-Net 的实用价值，我们在训练集未包含的 XPeng IRON 人形机器人上进行了分布外评估。如 Figure 10 所示，PTR-Net 对 IRON 机器人执行多种动作的类人性预测分数为 4.25，与人类标注者给出的平均分 4.36 高度吻合（误差仅 0.11）。这一结果初步表明，PTR-Net 学到的类人性评估能力并非简单记忆训练集中的特定机器人形态，而是捕捉了跨形态的运动学通用特征。然而，当前分布外验证仅覆盖个别新机器人，更广泛的新形态机器人测试尚未进行，该结论需要进一步验证。

![[assets/figures/papers/paper_list_l1045_https_arxiv_org_abs_2603_06181/figures/014_Figure_10.jpg]]
*Figure 10: Out-of-distribution evaluation on the XPeng IRON [62] humanoid robot*

### 失败模式与局限性

尽管 PTR-Net 在基准上表现优异，但分析中仍暴露出若干不足：

- **长时运动建模受限：** 数据集仅包含 5 秒片段，模型无法评估更长时序中的运动一致性变化或疲劳效应。
- **运动学表征的固有局限：** PTR-Net 仅依赖 SMPL-X 骨架的运动学数据，无法感知肌肉动力学、足底接触力或环境交互力等更精细的类人特征。某些机器人动作虽在运动学上接近人类，但动力学层面可能僵硬或不自然，模型对此无能为力。
- **主观标注偏差：** 类人性评分基于 25 名标注者的主观判断，虽经过一致性筛选（排除 5 名不一致者），但仍可能受文化背景和个人审美偏好的影响。不同文化群体对“自然动作”的认知差异尚未纳入考量。
- **动作类别覆盖不全：** 15 个动作类别无法涵盖所有实际应用场景，特别是精细操作和复杂地形适应等任务中的运动模式。

### 补充图表

![[assets/figures/papers/paper_list_l1045_https_arxiv_org_abs_2603_06181/figures/010_Table_3.jpg]]
*Table 3: Quantitative results for different models on the Motion Turing Test benchmark. “*” indicates VLM-based evaluation without task-specific training. Qwen3-VL-Plus (shot)* denotes that its results remain identical in DE/CGE/PED/DE-CoT/PA-CoT settings. “–” indicates invalid ρ due to constant outputs*

![[assets/figures/papers/paper_list_l1045_https_arxiv_org_abs_2603_06181/figures/006_Figure_5.jpg]]
*Figure 5: Overall distribution of motion human-likeness scores for human and humanoid motions (left) and human-likeness scores for humanoid in simulation and real scenarios (right)*

![[assets/figures/papers/paper_list_l1045_https_arxiv_org_abs_2603_06181/figures/009_Figure_6.jpg]]
*Figure 6: Representative SMPL-X sequences illustrate where humanoid robots perform poorly (upper part) and well (lower part)*

![[assets/figures/papers/paper_list_l1045_https_arxiv_org_abs_2603_06181/figures/011_Figure_8.jpg]]
*Figure 8: Four representative motion examples with PTR-Net predictions compared to human-annotated scores*

![[assets/figures/papers/paper_list_l1045_https_arxiv_org_abs_2603_06181/figures/012_Figure_9.jpg]]
*Figure 9: (a–b) Score distributions of human annotators and PTR-Net predictions for both human (imitating humanoid) and humanoid motions. (Bottom) Representative dance imitation pairs illustrating near-indistinguishable motion patterns*



## 定位与知识库关联

### 1. 评估范式的谱系定位

PTR-Net 的提出植根于人形机器人运动评估从“主观定性”向“客观定量”的范式迁移。传统上，运动类人性评估依赖人类观察者的整体印象，或基于特定任务指标（如步行速度、能耗）的间接推断，缺乏统一的、可复现的度量标准。该工作借鉴图灵测试的思想，将评估问题完全形式化为一个基于纯运动学数据（SMPL-X 骨架序列）的数值回归任务，这是其与现有工作最根本的差异。

该方法在评估范式谱系中占据一个独特的交叉位置：

- **相对于基于视觉语言模型（VLM）的评估方法**：Gemini 2.5 Pro、GPT-4o 等 VLM 方法代表了利用大规模预训练常识进行零样本/少样本评估的路线。PTR-Net 在 Motion Turing Test 基准上显著超越这些方法（MAE 0.5813 vs. Gemini 2.5 Pro PA-CoT 的 1.2682，Spearman's ρ 0.6841 vs. 0.2303），表明通用视觉常识推理在精细运动学质量判断任务上存在明显短板。VLM 方法缺乏对时序动态和骨架空间关系的专门建模能力，而 PTR-Net 通过时序编码器和图卷积结构弥补了这一缺陷。

- **相对于预训练骨架动作识别模型**：MotionBERT（Zhu et al., ICCV 2023）代表了从大规模骨架数据预训练、再在下游任务微调的迁移学习路线。PTR-Net 在 MAE 上以 0.5813 略优于 MotionBERT 的 0.6252，但优势幅度远小于相对 VLM 的差距。这说明预训练的骨架运动表征对于类人性评估具有较好的迁移能力，但专门为回归任务设计的时序-空间联合建模仍能带来额外增益。

- **相对于传统运动质量评估方法**：在运动生成领域，评估通常依赖 Fréchet Inception Distance（FID）等分布层面的指标，或人工评分。PTR-Net 提供了一个可训练的、实例级别的回归模型，能够对单个运动片段给出连续分数，这填补了分布度量与人工评分之间的空白。

### 2. 核心设计选择的因果机制

PTR-Net 的性能优势源于几个关键设计选择，消融实验揭示了其因果重要性：

- **时序编码器是性能的核心支柱**：移除双层双向 LSTM 时间编码器后，MAE 从 0.5813 升至 0.7631，RMSE 从 0.7926 升至 0.9691。这表明类人性判断高度依赖帧间的动态演化信息（节奏、加速度模式、运动过渡的流畅性），而非孤立姿态的静态特征。

- **无参数图邻接矩阵的自适应空间建模**：与常规可学习邻接矩阵的 GCN 或全连接 MLP 相比，无参数邻接矩阵的 ST-GCN 在消融中表现更优。该设计避免了参数化邻接矩阵可能带来的过拟合，同时保留了骨架关节间拓扑关系的归纳偏置，使得模型能更鲁棒地捕捉姿态协调性特征。

- **注意力池化与平滑正则化的协同**：注意力加权池化使模型能够自适应地关注对类人性判断最关键的时间段，而时序平滑正则化 $\mathcal{L}_{\mathrm{reg}}$ 抑制了预测在相邻帧间的剧烈波动。两者共同提升了预测的准确性和时序一致性，全模型在误差降低与排序一致性之间达到最佳平衡。

### 3. 适用边界与局限

PTR-Net 的适用范围和局限可从数据、模型和评估三个维度界定：

- **数据覆盖边界**：训练数据 HHMotion 包含 1000 个 5 秒片段、15 个动作类别、11 个机器人模型和 10 名人类被试。模型在分布内动作类别上表现可靠，但对于训练集中未出现的动作类型或更长时程的运动，其泛化能力尚未充分验证。尽管在 XPeng IRON 机器人上的分布外评估显示了初步的泛化潜力（预测分数 4.25 与人类评分 4.36 高度吻合），但这仅是个别案例，更广泛的新形态机器人测试仍然缺乏。

- **表征能力的根本局限**：PTR-Net 仅以 SMPL-X 骨架运动学作为输入，这意味着它无法捕获以下更高层次的类人性特征：（1）肌肉动力学和接触力——两个运动学上相似的步态可能因发力方式不同而产生截然不同的类人感知；（2）运动意图性和环境适应性——人类运动的类人性部分体现在对环境的灵活响应和目标导向性上，这些信息在纯骨架序列中丢失；（3）交互上下文——人类与物体或他人的交互质量是类人性的重要维度，但当前框架未涉及。

- **标注主观性的固有噪声**：类人性评分基于 25 名标注者的主观判断，尽管通过评分者间一致性检查排除了 5 名不一致标注者，但剩余标注者的判断仍可能受文化背景、个人审美偏好等因素影响。这种主观性为模型的训练目标引入了不可约的噪声上限。

### 4. 开放问题与后续工作方向

当前工作为运动图灵测试范式奠定了基础，但留下了若干值得探索的开放问题：

1. **超越运动学的类人性建模**：如何将意图性、适应性、任务上下文等高层次信息融入自动评估模型？可能的路径包括融合环境感知特征、引入任务完成度作为辅助监督信号，或利用视频级（而非纯骨架级）的多模态输入。

2. **基准的社区采纳与标准化**：运动图灵测试基准能否成为人形机器人运动生成与控制领域的通用评价标准，取决于社区的广泛采纳。这需要持续的基准维护、数据扩展，以及与其他评估范式的互补整合。

3. **分布外鲁棒性的系统验证**：随着更多开源机器人模型和形态的出现，PTR-Net 在新运动学结构上的鲁棒性需要系统性的评估。模型是否需要对每个新机器人形态进行微调，还是能够通过零样本泛化保持性能，是一个关键的实践问题。

4. **多维度评估体系的构建**：将类人性评分与任务完成度、能效、安全性等实际指标融合，形成更全面的机器人运动评估体系，是推动该领域从“看起来像人”走向“像人一样有效行动”的必经之路。



## 原文 PDF

![[paperPDFs/CVPR_2026/Towards_Motion_Turing_Test_Evaluating_Human_Likeness_in_Humanoid_Robots.pdf]]

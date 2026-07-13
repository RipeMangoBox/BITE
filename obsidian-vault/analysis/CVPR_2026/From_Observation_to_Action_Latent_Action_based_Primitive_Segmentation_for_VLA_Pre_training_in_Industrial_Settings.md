---
title: "From Observation to Action: Latent Action-based Primitive Segmentation for VLA Pre-training in Industrial Settings"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/From_Observation_to_Action_Latent_Action_based_Primitive_Segmentation_for_VLA_Pre_training_in_Industrial_Settings.pdf
project_link: "https://jiajiezhang7.github.io/latent-action-primitive-segmenter/"
code_link: null
aliases:
- LLABPS
tags:
- CVPR_2026
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
core_operator: 在抽象潜在动作空间中定义能量度量，而非依赖像素级变化，作为检测语义动作边界的关键信号。
primary_logic: 通过运动分词器将原始轨迹编码为潜在动作向量后，计算邻帧 L2 距离的「潜在动作能量」，能鲁棒捕获行为意图转变，抑制视觉噪声，实现无监督动作基元分割与发现。
claims:
- 在自建工业电机装配数据集上，LAPS 的 F1@2s 显著优于 ABD 和 OTAS 等无监督 TAD 基线
- 将运动分词器替换为 CLIP 特征或直接在原始速度上计算 E_action 会导致分割性能严重下降（F1@2s 从 87.5% 降至 25-27%）
- 基于 VLM 的簇内语义相似度 (ICSS) 确认所发现簇的语义一致性（0.926 vs 随机配对 0.804）
- Industrial Motor Assembly (Top-down View) 上 F1@2s = 81.27
---

# From Observation to Action: Latent Action-based Primitive Segmentation for VLA Pre-training in Industrial Settings

> [!tip] 核心洞察
> 通过运动分词器将原始轨迹编码为潜在动作向量后，计算邻帧 L2 距离的「潜在动作能量」，能鲁棒捕获行为意图转变，抑制视觉噪声，实现无监督动作基元分割与发现。

| 字段 | 内容 |
|------|------|
| 中文题名 | 基于潜在动作基元分割的工业VLA预训练：从观察到行动 |
| 英文题名 | From Observation to Action: Latent Action-based Primitive Segmentation for VLA Pre-training in Industrial Settings |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2511.21428) · [Project](https://jiajiezhang7.github.io/latent-action-primitive-segmenter/) |
| Topic | #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video |
| Method | LAPS (Latent Action-based Primitive Segmentation) |
| Dataset | Industrial Motor Assembly |

> [!tip] 效果简介
> - Industrial Motor Assembly (Top-down View) 上，F1@2s 81.27 vs ABD / OTAS (详见 Table 2) (显著优于无监督基线)。
> - Industrial Motor Assembly (Exocentric View) 上，F1@2s 81.93 vs ABD / OTAS (详见 Table 2) (显著优于无监督基线)。

## 概要

**问题瓶颈**：工业视觉-语言-动作（VLA）模型预训练面临严重的数据瓶颈——工厂车间存在大量连续工作视频流，但缺乏结构化动作标注，且难以自动提取语义动作基元。现有无监督时序动作检测方法依赖光流或视觉特征相似度，在工业场景中易受视觉噪声干扰，难以可靠捕获工人的行为意图转变。

**核心洞察**：本文提出 **LAPS（Latent Action-based Primitive Segmentation）**，其关键创新在于将动作分割从像素空间迁移到抽象潜在动作空间。通过训练轻量运动分词器将原始轨迹编码为量化潜在动作向量，定义「潜在动作能量」$E_{\mathrm{action}}(t) = \| z_{q,t} - z_{q,t-1} \|_2$ 作为邻帧 L2 距离，该信号能鲁棒捕获行为意图转变，同时抑制外观变化等视觉噪声。在此基础上，采用基于迟滞控制的双状态因果检测器定位动作边界，而非传统峰值检测算法。

**方法定位**：LAPS 属于无监督动作基元发现方法，其流水线包含四个模块：运动追踪（CoTracker 提取密集轨迹）→ 运动分词器（编码为离散动作 tokens）→ 动作检测与分割（潜在动作能量 + 迟滞控制器）→ 语义动作聚类（冻结 Transformer 嵌入 + 余弦 k-means）。该方法不依赖任何人工标注，仅需工作站任务数量的先验知识设定聚类数 k。

**主要结果**：在自建工业电机装配数据集上，LAPS 的 F1@2s 指标显著优于 **ABD**（Du et al., CVPR 2022）和 **OTAS**（Li et al., WACV 2024）等无监督基线；基于 VLM 的簇内语义相似度（ICSS）达到 0.926，验证了所发现动作基元的语义一致性。消融实验表明，将运动分词器替换为 CLIP 特征或在原始速度上计算能量会导致分割性能严重下降（F1@2s 从 87.5% 降至 25–27%），证实了专用运动编码与量化潜在空间的关键作用。

**局限与展望**：当前方法仅验证于高度重复的工业制造任务，向动作多样性高的非结构化环境（家庭、医疗）扩展仍需探索；从被动观察到的动作基元到机器人实际执行之间的策略学习与技能对齐是后续重要方向。



### 工业 VLA 面临的动作数据瓶颈

视觉-语言-动作（VLA）模型在通用机器人操作中展现出巨大潜力，但其在工业场景的落地面临一个根本性瓶颈：**严重缺乏结构化的动作数据**。工业制造环境产生海量连续工作视频流，然而这些数据几乎全部处于未标记状态——人工标注每一段视频中每个动作的起止边界和语义类别，成本极高且不可扩展。现有 VLA 预训练范式高度依赖大规模、带细粒度动作标注的数据集，这一供需矛盾直接制约了工业 VLA 的发展。

更关键的是，从连续视频流中自动提取动作基元（action primitives）本身就是一个开放难题。传统方法通常依赖光流或视觉特征相似度作为分割信号，但这些信号反映的是像素级物理运动，而非任务层面的语义意图转变。正如 Figure 4 所示，光流信号充满噪声，难以区分“有意义的动作切换”与“无意义的运动波动”，导致分割结果与真实任务边界严重错位。

### 现有无监督方法的局限

当前无监督动作边界检测方法，如 **ABD**（Du et al., CVPR 2022）和 **OTAS**（Li et al., WACV 2024），在设计上主要面向日常活动视频（如烹饪、早餐准备），其分割信号源（视觉特征相似度或光流变化）在工业场景中面临两个根本性挑战：

1. **视觉噪声干扰严重**：工业环境中存在大量重复性运动、遮挡和视角变化，像素级信号极易被高频噪声淹没，难以稳定捕获语义动作边界。
2. **语义与运动的解耦缺失**：这些方法缺乏将“物理运动”映射到“行为意图”的抽象表示层，导致分割出的片段往往在物理层面连续、在语义层面却支离破碎。

### 核心动机与研究思路

本文的核心动机在于：**工业 VLA 预训练亟需一种能够从无标注连续视频中自动发现、分割并聚类语义动作基元的方法，且该方法必须对工业环境中的视觉噪声具有鲁棒性。**

为此，本文提出一个关键洞察：**将动作分割的信号源从像素空间迁移到抽象的潜在动作空间**。通过训练一个轻量级运动分词器（motion tokenizer），将原始运动轨迹编码为潜在动作向量，再在量化后的潜在空间中定义“潜在动作能量”（Latent Action Energy）作为边界检测信号。这一设计使得分割过程能够抑制视觉噪声，直接捕获行为意图的转变点，而非物理运动的变化点。

基于此，LAPS（Latent Action-based Primitive Segmentation）流水线以完全无监督的方式，从原始视频流中输出结构化的动作序列（离散动作码、分割片段、语义簇），为下游 VLA 预训练提供可直接使用的结构化动作数据。



## 核心方法与创新机理

工业 VLA 预训练面临的核心瓶颈在于：大量连续工作视频流缺乏结构化动作标注，传统方法依赖像素级变化（如光流）或通用视觉特征（如 CLIP）难以鲁棒地捕获语义动作边界。LAPS 通过三个关键创新突破这一困境：

### 1. 潜在动作能量：从像素空间到抽象动作空间的信号迁移

传统无监督动作边界检测方法（如 **ABD** (Du et al., CVPR 2022)、**OTAS** (Li et al., WACV 2024)）通常以光流或视觉特征相似度作为分割信号，这类信号对光照变化、遮挡和无关背景运动高度敏感，难以区分“有意义的动作切换”与“视觉噪声”。

LAPS 的核心洞察在于：**动作边界的本质是行为意图的转变，而非像素级运动的突变**。为此，论文提出在抽象潜在动作空间中定义分割信号——**潜在动作能量 (Latent Action Energy)**：

$$E_{\mathrm{action}}(t) = \| z_{q,t} - z_{q,t-1} \|_2$$

其中 $z_{q,t}$ 是运动分词器输出的量化潜在动作向量。该度量的因果机制在于：运动分词器通过在大规模短视频片段上训练，学会了将原始运动轨迹压缩为对行为动态敏感的紧致表示，从而使得 $E_{\mathrm{action}}$ 在动作执行期间呈现持续高能，在语义边界处急剧下降（Figure 4 定性对比印证了这一点）。

**消融实验提供了决定性证据**（Table 5）：将信号源替换为 CLIP 视觉特征或直接在原始速度上计算 $E_{\mathrm{action}}$，严格 F1@2s 指标从 87.5% 骤降至 25–27%，簇内语义相似度 (ICSS) 从 0.92 跌至 0.75。这证实了专用运动编码和量化潜在空间对于鲁棒动作发现是不可替代的。

### 2. 基于迟滞控制的因果动作检测器

传统方法通常采用峰值检测或局部极小值来定位动作边界，这类算法对信号噪声敏感，容易产生碎片化分割或漏检。

LAPS 将动作检测建模为**因果双状态 (ON/OFF) 控制器**，引入迟滞控制机制：当指数滑动平均平滑后的能量信号 $y_t = \alpha E_{\mathrm{action}}(t) + (1-\alpha) y_{t-1}$ 超过上阈值时进入 ON 状态（动作执行中），低于下阈值时回到 OFF 状态（动作完成）。这种设计的关键优势在于：(1) 因果性保证了在线流式场景的可部署性；(2) 迟滞区间抑制了能量波动引起的状态抖动，产生稳定、语义完整的动作段。

### 3. 训练无关的冻结 Transformer 序列嵌入

动作段聚类面临的核心挑战是变长潜在向量序列的语义聚合。基线方法通常采用均值池化或需要额外训练的编码器，前者丢失时序结构信息，后者违背无监督前提。

LAPS 提出使用**随机初始化且冻结的轻量 Transformer 编码器**（L=4 层，H=4 头），通过前向推理将变长潜在序列映射为固定维度的段嵌入 $e_i = \frac{1}{T_i} \sum_t h_t^{(L)}$，再经余弦 k-means 聚类发现有限动作集。该设计无需任何训练或标注，却能在 Transformer 的自注意力机制中隐式捕获动作内部的时序依赖。

消融实验（Table 5）表明，冻结 Transformer 编码器相比均值池化基线将聚类 ICSS 从 0.84 提升至 0.92，验证了时序建模对语义聚合的关键作用。

### 创新总结

LAPS 的三项创新构成了一条因果链路：**潜在动作能量**将分割信号从不可靠的像素空间迁移至语义敏感的抽象动作空间；**迟滞控制器**以因果、鲁棒的方式将该信号转化为稳定动作段；**冻结 Transformer 嵌入**在无监督约束下最大化动作段的语义可分性。三者协同实现了从连续视频流到结构化动作词汇的端到端无监督发现，为工业 VLA 预训练提供了可扩展的数据引擎。



LAPS (Latent Action-based Primitive Segmentation) 是一个面向工业 VLA 预训练的无监督动作基元发现流水线。其核心设计动机在于：工业场景中大量连续工作视频流缺乏结构化动作标注，传统基于像素级视觉特征的分割方法难以鲁棒捕获行为意图的转变。LAPS 通过在抽象潜在动作空间中定义能量度量，将“动作边界检测”从视觉噪声敏感的像素域迁移到语义感知的运动潜空间，从而实现对动作基元的无监督分割与聚类。

流水线由三个顺序阶段构成（Figure 2），形成从原始视频到结构化动作词汇的端到端处理链路：

![[assets/figures/papers/paper_list_l2493_https_arxiv_org_abs_2511_21428/figures/002_Figure_2.jpg]]
*Figure 2: Overview of the LAPS pipeline: (1) Motion Tracking extracts motion keypoints from raw video using a point tracker. (2) Action Detection & Segmentation generates a latent vector stream via a motion tokenizer and identifies action boundaries to segment latent vectors, video clips, and action codes. (3) Semantic Action Clustering groups the segmented latent vectors into meaningful semantic action clusters*

1. **运动追踪 (Motion Tracking)**：使用点追踪器（如 CoTracker）从原始视频中提取密集运动轨迹，将像素级视觉信息压缩为稀疏但信息丰富的运动关键点流。这一步骤将视觉外观变化转化为结构化的运动信号，为后续的潜在动作编码提供输入。

2. **动作检测与分割 (Action Detection & Segmentation)**：这是 LAPS 的核心模块，包含运动分词、能量计算和边界检测三个子步骤。首先，轻量级运动分词器 $M_{\theta}$ 将运动轨迹编码为量化潜在动作向量流 $z_{q,t}$，并通过滑动窗口机制将视频转换为离散动作代码序列 $c_t \in \{0, \ldots, 2047\}$（Figure 3）。然后，在量化潜空间中计算相邻帧的 L2 距离，定义**潜在动作能量** $E_{\mathrm{action}}(t) = \| z_{q,t} - z_{q,t-1} \|_2$，作为衡量运动动态变化强度的信号。最后，基于迟滞控制的双状态 (ON/OFF) 因果状态机在该能量信号上检测动作边界，将视频分割为语义动作片段及其对应的潜在向量和动作代码。

3. **语义动作聚类 (Semantic Action Clustering)**：将分割得到的变长潜在向量序列通过冻结的随机初始化 Transformer 编码器嵌入为固定长度的段级表示 $e_i = \frac{1}{T_i} \sum_t h_t^{(L)}$，然后采用余弦 k-means 聚类将海量动作片段归纳为有限的动作词汇，完成从连续观测到离散动作基元的抽象。

流水线的关键设计决策在于**信号源的选择**：动作边界检测不依赖光流或通用视觉特征（如 CLIP），而是严格定义在运动分词器的量化潜空间中。消融实验（Table 5）表明，将运动分词器替换为 CLIP 特征或直接在原始速度上计算 $E_{\mathrm{action}}$ 会导致分割性能严重下降（F1@2s 从 87.5% 降至 25–27%），验证了专用运动编码的必要性。这一设计的直觉在于：量化潜空间通过有限标量量化 (FSQ) 将连续运动动态离散化为语义感知的动作代码本，使得能量信号能鲁棒捕获行为意图的转变，同时抑制光照、纹理等视觉噪声的干扰（Figure 4 定性展示了潜在动作能量相比光流在语义边界检测上的优势）。

### 补充图表

![[assets/figures/papers/paper_list_l2493_https_arxiv_org_abs_2511_21428/figures/001_Figure_1.jpg]]
*Figure 1: Example of our segmentation approach using Latent Action Energy from a Motion Tokenizer. Action boundaries (red circles) correspond to transitions from high energy to baseline, indicating action completion. The pipeline outputs the Latent Action Sequence (bottom codes), providing structured representations for VLA pre-training*



### 3.1 潜在动作能量：核心分割信号

LAPS 的核心创新在于将动作分割的信号源从像素空间迁移至抽象潜在动作空间。传统无监督动作边界检测方法（如 **ABD** (Du et al., CVPR 2022)、**OTAS** (Li et al., WACV 2024)）通常依赖光流或视觉特征的相似度变化来定位边界，但这些信号对光照变化、相机抖动和外观噪声高度敏感，难以鲁棒捕获语义层面的动作转换。

LAPS 的关键洞察是：**在量化潜在空间中，相邻时间步的 L2 距离能够有效反映运动动态的语义变化强度，同时抑制视觉噪声。** 这一度量被定义为「潜在动作能量」（Latent Action Energy）：

$$E_{\mathrm{action}}(t) = \| z_{q,t} - z_{q,t-1} \|_2$$

其中：
- $z_{q,t}$ 表示时间步 $t$ 经运动分词器编码并量化后的潜在动作向量；
- $E_{\mathrm{action}}(t)$ 量化了 $t-1$ 到 $t$ 之间运动动态的变化幅度。

该公式的因果机制在于：运动分词器 $M_\theta$ 通过在大规模短视频片段上的训练，学会了将原始运动轨迹压缩为紧凑的离散潜在表示。在这个表示空间中，连续的、语义一致的动作片段内部动态变化较小，而动作转换（如从“抓取”切换到“装配”）则对应运动模式的剧烈变化，表现为潜在空间中较大的位移。图 4 的定性对比验证了这一机制：潜在动作能量在真实语义边界处呈现清晰的持续峰值和急剧回落，而光流信号则充满高频噪声，仅反映物理运动而非任务阶段。

### 3.2 因果平滑与迟滞控制器

原始 $E_{\mathrm{action}}(t)$ 信号仍包含高频噪声，直接用于边界检测会产生大量伪边界。LAPS 采用指数滑动平均（EMA）进行因果平滑，确保不泄露未来信息：

$$y_t = \alpha E_{\mathrm{action}}(t) + (1-\alpha) y_{t-1}$$

其中 $\alpha$ 为平滑系数，控制历史信息的衰减速度。

在平滑后的能量信号上，LAPS 不采用传统的峰值检测或局部极小值算法，而是引入一个**基于迟滞控制的双状态（ON/OFF）因果状态机**作为动作检测器。该控制器设定两个阈值：高阈值触发动作开始（ON 状态），低阈值标记动作结束（OFF 状态）。迟滞机制防止了信号在阈值附近的抖动引起的状态频繁切换，从而产生稳定、连贯的动作段分割。这一设计的关键优势在于其因果性——决策仅依赖当前和过去的信息，适用于在线流式场景。

### 3.3 段级嵌入与聚类

分割得到的每个动作段对应一个变长的量化潜在向量序列 $S_{q,i} \in \mathbb{R}^{T_i \times d}$。为进行语义聚类，LAPS 使用一个**冻结的随机初始化 Transformer 编码器**将其嵌入为固定长度的段表示：

$$e_i = \frac{1}{T_i} \sum_t h_t^{(L)}$$

其中：
- $h_t^{(L)}$ 为 Transformer 第 $L$ 层（末层）在时间步 $t$ 的隐状态；
- $T_i$ 为第 $i$ 个动作段的帧数；
- $e_i$ 为通过时序均值池化得到的段级嵌入。

消融实验（Table 5）表明，该冻结 Transformer 编码器显著优于直接均值池化基线（聚类 ICSS 从 0.84 提升至 0.92），原因在于 Transformer 的自注意力机制能够捕获段内潜在动作码之间的时序依赖关系，即使未经训练也能提供更丰富的上下文表示。

### 3.4 语义一致性评估

为量化聚类发现的语义质量，LAPS 引入簇内语义相似度（ICSS）指标：

$$\mathrm{ICSS}_k = \frac{1}{|\mathcal{P}_k|} \sum_{(i,j) \in \mathcal{P}_k} \cos(v_i, v_j)$$

其中：
- $\mathcal{P}_k$ 为第 $k$ 个簇内所有样本对的集合；
- $v_i$ 为样本 $i$ 对应视频片段经预训练视觉语言模型（VLM）提取的嵌入向量；
- $\cos(\cdot,\cdot)$ 为余弦相似度。

ICSS 通过外部 VLM 作为语义裁判，评估同一簇内片段的视觉语义一致性。Table 4 显示 LAPS 发现簇的 ICSS 达到 0.926，远高于随机配对的基线 0.804，验证了所发现动作基元的语义内聚性。

### 补充图表

![[assets/figures/papers/paper_list_l2493_https_arxiv_org_abs_2511_21428/figures/003_Figure_3.jpg]]
*Figure 3: Sliding-window tokenization: A motion tokenizer converts the video stream into a sequence of discrete latent action indices*

![[assets/figures/papers/paper_list_l2493_https_arxiv_org_abs_2511_21428/figures/004_Figure_4.jpg]]
*Figure 4: Qualitative comparison of our*



## 实验与关键发现

### 主实验：工业场景下的动作基元分割

LAPS 的核心能力首先在自建的工业电机装配数据集上得到验证。该数据集包含约 10 小时的连续视频，从顶视（Top-down View）和外视（Exocentric View）两个同步视角记录工人执行装配任务的全过程。评估采用严格的时间对齐指标 F1@2s，即预测边界与真值边界偏差在 ±2 秒内视为正确检测。

在 Top-down View 上，LAPS 取得 **81.27** 的 F1@2s，在 Exocentric View 上达到 **81.93**，显著优于无监督动作边界检测基线 **ABD**（Du et al., CVPR 2022）和 **OTAS**（Li et al., WACV 2024）（Table 2）。这一优势源于潜在动作能量在抽象运动空间中对语义边界的鲁棒捕获能力——Figure 4 的定性对比清晰展示了这一点：潜在动作能量（蓝色曲线）在动作执行期间呈现持续高峰，在真值语义边界处急剧回落至基线；而光流信号（红色曲线）充满高频噪声，仅反映物理运动幅度，无法区分任务阶段转换。

![[assets/figures/papers/paper_list_l2493_https_arxiv_org_abs_2511_21428/figures/007_Table_2.jpg]]
*Table 2: Comparison on the Industrial Motor Assembly*

在公共基准数据集上的表现（Table 1）进一步验证了方法的泛化潜力：LAPS 在 GTEA 和 Breakfast 数据集上与无监督时序动作检测（TAD）基线相比展现了竞争力，表明基于潜在动作能量的分割策略并非仅对高度重复的工业任务有效。

![[assets/figures/papers/paper_list_l2493_https_arxiv_org_abs_2511_21428/figures/006_Table_1.jpg]]
*Table 1: Comparison on GTEA [14] and Breakfast [19]*

### 消融研究：流水线各组件的因果贡献

Table 5 的系统消融揭示了 LAPS 各模块对分割和聚类性能的因果影响，所有结果均来自 Exocentric View 测试集，使用严格的 F1@2s 指标。

![[assets/figures/papers/paper_list_l2493_https_arxiv_org_abs_2511_21428/figures/009_Table_5.jpg]]
*Table 5: Ablation study on pipeline components, showing their impact on segmentation and clustering. Segmentation is evaluated using the strict F1@2s metric. Results are from the Exocentric View test set*

**信号源与表示层的关键性。** 将运动分词器替换为通用视觉特征（如 CLIP 嵌入）会导致分割性能灾难性下降：F1@2s 从完整管道的 **87.5%** 骤降至 **27.2%**，聚类语义一致性 ICSS 也从 0.92 跌至 0.75。这证明了专用运动编码器对捕获动作语义的必要性——通用视觉特征虽能编码场景外观，却无法抽象出与行为意图相关的运动动态。更深层的证据来自信号源消融：若在预量化潜在表示或原始运动速度上直接计算潜在动作能量，F1@2s 仅约 **25%**，说明量化潜在空间中的 L2 距离才是有效的语义边界信号。量化过程本身起到了信息瓶颈的作用，滤除了与动作语义无关的运动变化。

**迟滞控制器的必要性。** 将因果双状态控制器替换为常规峰值检测算法后，分割性能显著下降（Table 5 中 w/o Hysteresis 变体）。迟滞机制通过 ON/OFF 双状态和阈值滞后，有效抑制了能量信号中的短暂波动导致的虚假边界检测，这是传统峰值检测无法实现的鲁棒性。

**时序编码对聚类质量的决定性作用。** 用于聚类的冻结 Transformer 编码器显著优于均值池化基线：聚类 ICSS 从 0.84 提升至 **0.92**（Table 5 中 w/o Transformer 变体）。Table 3 进一步展示了冻结 Transformer 嵌入在多个聚类指标上的全面优势，验证了即使不进行训练，Transformer 的时序建模能力也能有效捕获变长潜在序列中的动作语义结构。Figure 5 的 UMAP 可视化确认了聚类结果在嵌入空间中形成清晰分离的簇，且经人工核验与真实工作站任务对应。

### 语义一致性验证

为弥补无监督聚类缺乏外部真值的局限，LAPS 引入基于视觉语言模型（VLM）的簇内语义相似度指标 ICSS（Table 4）。在 Exocentric View 数据集上，发现的动作簇 ICSS 达到 **0.926**，而随机配对的基线仅为 **0.804**，表明所发现的簇在 VLM 语义空间中具有显著高于随机水平的内部一致性。这一外部验证增强了对无监督发现动作词汇语义有效性的信心，但需注意该度量依赖单一预训练 VLM，其评估可能受 VLM 自身先验偏差影响，尚未在多个 VLM 上交叉验证。

![[assets/figures/papers/paper_list_l2493_https_arxiv_org_abs_2511_21428/figures/010_Table_4.jpg]]
*Table 4: VLM-based Semantic Coherence (ICSS): Mean intracluster similarity (± std) for discovered clusters. The baseline samples random pairs from the entire dataset irrespective of clusters and thus, by definition, only provides a single Overall metric for comparison*

### 失败模式与局限性

尽管 LAPS 在工业场景中表现优异，其设计假设和验证范围指向若干明确的失败模式：

1. **动作多样性受限。** 当前验证仅限于高度重复的工业制造任务，动作模式单一且工作站任务边界清晰。对于动作模式多变、任务交错频繁的非结构化环境（如日常家务或医疗操作），潜在动作能量是否仍能保持清晰的语义边界检测能力尚属未知。

2. **聚类数依赖人工先验。** 动作聚类数量 k 依据工作站任务数量的先验知识设定，未提出自动确定最优聚类数的机制。在任务数量未知或动态变化的场景中，这一依赖将构成瓶颈。

3. **阈值与窗口的静态设定。** 全流水线仍依赖固定窗口和预设阈值（包括迟滞控制器的 ON/OFF 阈值），在长时间在线流式场景下的稳定性需进一步评估。能量信号的分布可能随场景光照、相机视角或任务节奏变化而漂移，静态阈值对此缺乏适应能力。

4. **数据集规模有限。** 工业电机装配数据集约 10 小时，泛化到大规模、多样化的工业场景仍需进一步验证。

### 补充图表

![[assets/figures/papers/paper_list_l2493_https_arxiv_org_abs_2511_21428/figures/005_Figure_5.jpg]]
*Figure 5: UMAP visualization of action primitive embeddings colored by k-means cluster ID. Distinct, well-separated clusters that correspond to real workstation tasks confirmed through manual inspection*

![[assets/figures/papers/paper_list_l2493_https_arxiv_org_abs_2511_21428/figures/008_Table_3.jpg]]
*Table 3: Clustering results on the Exocentric View dataset (6,444 segments, k = 3), comparing our Frozen Transformer embedding with a strong non-temporal aggregation baseline*



## 定位与知识库关联

### 1. 问题定位：工业 VLA 预训练的数据瓶颈

视觉-语言-动作（VLA）模型在机器人操控领域展现出巨大潜力，但其预训练严重依赖大规模、结构化标注的动作数据。在工业制造场景中，这一瓶颈尤为突出：工厂工作站通常配备连续录制的视频监控系统，积累了大量未标记的连续工作视频流，但从中自动提取语义上有意义的动作基元（action primitives）仍是一个开放难题。现有方案要么依赖昂贵的人工标注，要么采用光流或视觉特征相似度等像素级变化信号进行无监督分割——这些信号对光照变化、相机抖动和外观噪声高度敏感，难以鲁棒地捕获行为意图的语义转变。

LAPS 正是在这一背景下被提出。其核心主张是：**动作边界的检测不应在原始像素空间进行，而应在一个抽象、高维的潜在动作空间（latent action space）中完成**。这一主张直接回应了工业数据的特点——高度重复的制造任务、相对固定的工作站视角、以及动作语义与视觉外观之间的弱耦合关系。

### 2. 与无监督时序动作检测基线的关系

LAPS 在无监督时序动作检测（Temporal Action Detection, TAD）这一任务线上与两类基线方法形成直接对比：

| 基线方法 | 核心信号 | 代表性工作 | 与 LAPS 的关键差异 |
|----------|----------|------------|-------------------|
| 基于光流/视觉特征 | 光流幅值、视觉特征相似度 | **ABD** (Du et al., CVPR 2022)、**OTAS** (Li et al., WACV 2024) | 信号源在像素/特征空间，对视觉噪声敏感 |
| 基于通用视觉表示 | CLIP 等预训练视觉编码器特征 | 本文消融实验中的 CLIP 变体 | 缺乏对运动动态的专用建模 |

**定量对比**（Table 2, Industrial Motor Assembly 数据集）：

- **Top-down View**：LAPS 的 F1@2s 达到 81.27，显著优于 ABD 和 OTAS 等无监督基线。
- **Exocentric View**：LAPS 的 F1@2s 达到 81.93，同样保持显著优势。

**关键消融证据**（Table 5）进一步揭示了信号源选择的决定性作用：

- 将运动分词器替换为 CLIP 特征后，F1@2s 从 87.5%（Full Pipeline）骤降至 **27.2%**，簇内语义相似度（ICSS）从 0.92 降至 0.75。
- 在预量化潜在表示或原始速度上计算 $E_{\mathrm{action}}$，F1@2s 仅为约 **25%**。

这些结果表明：**专用运动编码（motion tokenizer）和量化潜在空间是 LAPS 性能的不可替代组件**，通用视觉表示无法捕获工业场景中细微但语义关键的运动动态。

### 3. 与动作分词器方法的关系

LAPS 的运动分词器（Motion Tokenizer）架构主要源自 **AMPLIFY**（时序量化自编码器），但 LAPS 的创新不在于分词器本身，而在于**如何利用分词器输出的量化潜在向量流来定义无监督分割信号**。具体而言：

- AMPLIFY 等动作分词器方法（如 TAPIR、CoTracker 的后续工作）关注的是将运动轨迹压缩为离散 tokens，用于生成式建模或动作预测。
- LAPS 则将这些离散 tokens 对应的连续量化向量 $z_{q,t}$ 作为中间表示，在其上定义潜在动作能量 $E_{\mathrm{action}}(t) = \| z_{q,t} - z_{q,t-1} \|_2$，将分词器从「生成工具」转化为「边界检测的特征提取器」。

这一设计选择的因果机制在于：量化潜在空间的有限码本（codebook size = 2048）天然地对视觉外观变化进行了信息压缩，使得 $E_{\mathrm{action}}$ 主要反映运动动态的实质性转变，而非像素级的噪声波动。Figure 4 的定性对比直观展示了这一优势：潜在动作能量（蓝色曲线）在动作执行期间呈现清晰、持续的峰值，在真实语义边界处出现急剧下降；而光流信号（红色曲线）充满高频噪声，仅反映物理运动而非任务阶段。

### 4. 在 VLA 预训练知识库中的定位

从 VLA 预训练的宏观视角看，LAPS 填补了「从原始视频流到结构化动作序列」这一关键空白。其输出——**潜在动作序列（Latent Action Sequence）**——直接服务于下游 VLA 模型的动作 token 预训练，类似于语言模型中文本分词器的角色，但专门针对工业操控的动作语义。

与现有 VLA 数据管线的对比：

| 方法/管线 | 动作表示 | 标注需求 | 适用场景 |
|-----------|----------|----------|----------|
| RT-2 等 | 离散化动作 tokens | 需要动作标注 | 通用机器人操控 |
| 基于关键帧的人工标注 | 人工定义的语义边界 | 需要大量人工 | 小规模特定任务 |
| **LAPS** | 自动发现的潜在动作 tokens | **无需动作标注** | 工业重复性任务 |

LAPS 的独特贡献在于：在完全不依赖动作标注的条件下，从连续视频流中自动发现语义一致的动作基元，并以离散 token 序列的形式输出，使其可以直接接入现有 VLA 架构的动作预训练流程。这一能力对于大规模工业部署具有实际价值——工厂已有的监控视频可以直接转化为训练数据，无需额外的人工标注投入。

### 5. 适用边界与局限

基于论文中的实验设置和消融分析，LAPS 的适用边界和局限可归纳如下：

**已验证的适用条件**：

- **高度重复的工业制造任务**：实验在电机装配场景中进行，动作模式相对固定、工作站布局稳定。
- **固定或有限视角**：使用 Top-down 和 Exocentric 两个同步视角，均为固定机位。
- **中等时长视频流**：数据集约 10 小时，测试子集约 2 小时。

**已识别的局限**：

1. **泛化能力未知**：当前方法仅验证于高度重复的工业制造任务。对于动作模式多变、背景动态复杂的非结构化环境（如家庭、医院），其分割质量和语义一致性尚未得到验证。这是一个需要手动验证的风险点。

2. **聚类数依赖先验知识**：动作聚类的数量 $k$ 基于工作站任务数量的先验知识设定，论文未提出自动确定最优聚类数的机制。在实际部署中，若任务种类未知或动态变化，这一限制将影响方法的自动化程度。

3. **阈值敏感性**：动作检测器采用基于迟滞控制的 ON/OFF 状态机，依赖预设阈值。虽然论文提到阈值通过自监督伪标签优化，但在线流式场景下的长时间稳定性和跨场景阈值迁移能力仍需进一步评估。

4. **语义一致性评估的单一性**：ICSS 指标依赖单一预训练 VLM（视觉语言模型），其度量可能受 VLM 自身先验偏差的影响，论文未在多个 VLM 上进行交叉验证。

5. **数据集规模有限**：约 10 小时的视频数据对于验证方法的有效性是足够的，但泛化到大规模、多样化的工业场景仍需进一步验证。

### 6. 开放问题

论文揭示或未解决的开放问题包括：

1. **跨领域泛化**：如何将 LAPS 扩展至动作多样性高的非工业领域（如日常家务或医疗操作），同时保持语义一致性？这可能需要重新审视运动分词器的训练数据分布和潜在动作空间的结构。

2. **从观察到执行的闭环**：从被动观察到的动作基元到机器人实际操作执行之间，如何实现策略学习与技能对齐？LAPS 目前仅解决「观察-理解」阶段，尚未涉及「理解-执行」的映射。

3. **多模态增强**：是否可以引入多模态信息（如语言叙述、操作手册文本）提升发现动作词汇的语义精度和可解释性？这可能是连接无监督动作发现与下游任务指令理解的关键桥梁。

4. **在线自适应**：在流式场景下，如何使动作检测阈值和聚类结构自适应地随任务分布变化而调整，而非依赖离线预定义的参数？

5. **评估基准的标准化**：工业 VLA 预训练领域缺乏统一的评估基准。LAPS 的自建数据集和 ICSS 指标提供了初步尝试，但社区需要更系统、更多样的基准来推动方法比较和进步。



## 原文 PDF

![[paperPDFs/CVPR_2026/From_Observation_to_Action_Latent_Action_based_Primitive_Segmentation_for_VLA_Pre_training_in_Industrial_Settings.pdf]]

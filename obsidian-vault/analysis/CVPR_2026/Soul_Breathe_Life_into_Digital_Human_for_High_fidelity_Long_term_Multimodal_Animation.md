---
title: "Soul: Breathe Life into Digital Human for High-fidelity Long-term Multimodal Animation"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Soul_Breathe_Life_into_Digital_Human_for_High_fidelity_Long_term_Multimodal_Animation.pdf
project_link: null
code_link: null
aliases:
- Soul
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 基于聚类码本的阈值感知替换策略（threshold-aware codebook replacement），在生成过程中将偏离分布的潜在特征约束回训练分布附近，从而抑制时序退化。
primary_logic: 利用训练潜在特征构建离散码本，并通过阈值机制在长时生成中柔性校正离群特征，既保持身份与场景一致性，又避免突变伪影。
claims:
- 长时推理中出现颜色偏移和细节丢失，阈值感知码本替换可有效缓解（图7）。
- Soul 可生成最长 4 分钟的身份一致视频（图6顶部）。
- Soul 在 Soul-Bench 的视频文本一致性、唇同步、身份保持等指标上全面超越现有开源和商业方案（表2）。
- Soul-Bench 上 Video-Text Consistence↑ = 4.85
---

# Soul: Breathe Life into Digital Human for High-fidelity Long-term Multimodal Animation

> [!tip] 核心洞察
> 利用训练潜在特征构建离散码本，并通过阈值机制在长时生成中柔性校正离群特征，既保持身份与场景一致性，又避免突变伪影。

| 字段 | 内容 |
|------|------|
| 中文题名 | Soul：为高保真长时多模态数字人动画注入生命力 |
| 英文题名 | Soul: Breathe Life into Digital Human for High-fidelity Long-term Multimodal Animation |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2512.13495) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | Soul |
| Dataset | Soul-Bench, Efficiency |

> [!tip] 效果简介
> - Soul-Bench 上，Video-Text Consistence↑ 4.85 vs 4.77 (StableAvatar) (+0.08)；LSE-D↓ 0.130 vs 0.663 (Sonic) (-0.533)；LSE-C↑ 6.82 vs 8.48 (InfiniteTalk) (-1.66)。
> - Efficiency (109×1088×1920, 单 GPU) 上，推理加速比 11.4× （89.4 s） vs 1.0× （无优化，约 1020 s） (+10.4×)。

## 概要

Soul 是一个面向高保真、长时多模态数字人动画的生成框架，旨在解决现有方法在**长时推理中因潜在特征分布漂移导致的身份漂移与语义质量退化**问题。其核心创新在于提出了一种**基于聚类码本的阈值感知替换策略**：利用训练数据构建离散潜在特征码本，在生成过程中将偏离分布的离群特征柔性约束回训练分布附近，从而在保持身份与场景一致性的同时抑制颜色偏移与细节丢失。

方法上，Soul 以 **Wan2.2-5B** 为基础视频模型，通过新增 Audio-Attention 层注入 Whisper 音频特征以驱动唇形与表情，并引入关键帧复制、片段间潜在帧重叠与阈值感知码本替换三项策略实现长时一致性生成。在推理效率方面，Soul 结合步数/CFG 联合蒸馏与轻量化 eVAE 解码器，在性能损失可忽略的前提下实现 **11.4 倍加速**。

实验方面，Soul 在自建基准 **Soul-Bench** 上全面超越现有开源方案（如 Sonic、StableAvatar、EchoMimicV3 等）与商用产品（HeyGen、Kling-Avatar），在视频文本一致性、唇同步精度、身份保持与视频质量等指标上均取得最优结果，同时支持最长 **4 分钟**的身份一致视频生成。



数字人动画旨在根据多模态驱动信号（文本、音频等）生成语义一致、身份保持的人类视频，其应用涵盖虚拟主播、数字分身、交互式助手等场景。然而，现有方法在实现**高保真长时生成**方面仍面临显著瓶颈。

### 核心瓶颈：长时推理中的潜在特征漂移

当前主流方案通常将长视频分割为独立片段逐段生成，再通过简单的帧重叠拼接。这种策略在短时生成中尚可维持质量，但随着时间推移，**潜在特征分布会逐渐偏离训练分布**，导致两类典型退化现象：

1. **身份漂移**：人物面部特征、肤色、发型等属性在长序列中逐渐变化，破坏视觉一致性。
2. **语义质量退化**：出现颜色偏移、细节丢失等伪影，尤其在复杂场景切换时更为明显。

Figure 7 直观展示了这一问题：即使片段间存在帧重叠，生成视频随时间仍会出现意外的颜色偏差和细节损失。本质上，这是由于扩散模型在迭代采样过程中，缺乏将偏离分布的中间潜在特征约束回训练分布的有效机制。

### 数据层面的缺口

现有训练数据存在两方面不足：
- **场景多样性有限**：多数数据集聚焦于固定背景下的单人讲话，缺乏多场景、多动作的覆盖，导致模型泛化能力受限。
- **细粒度标注缺失**：缺乏对动作类型、场景语义、音频-视频对齐的精细标注，难以支撑多模态语义一致的训练目标。

### 本文动机

针对上述瓶颈，本文提出 **Soul** 框架，核心思路是：

- **构建大规模多样化数据集 Soul-1M**：通过自动化筛选管线收集覆盖多场景、多动作的人类视频数据，并辅以混合模态训练策略增强泛化性。
- **引入阈值感知码本替换机制**：利用训练数据的潜在特征构建离散码本，在长时生成中通过阈值机制柔性校正离群特征，从根源上抑制潜在特征漂移。
- **兼顾效率优化**：通过步数/CFG 联合蒸馏与轻量化 eVAE 解码器，在保持生成质量的前提下实现显著的推理加速。

Soul 的目标是在**身份一致性、语义保真度、长时稳定性**三个维度上同时取得突破，使数字人动画从“短时可用”迈向“长时可信”。



## 核心方法与创新机理

Soul 的核心创新并非单一算法突破，而是针对**长时多模态数字人动画**场景，在现有 Wan2.2-5B 视频生成基座上系统性重构了三个关键环节：音频注入方式、长时生成策略与推理效率。这三项改造直指当前数字人动画的瓶颈——**长时推理中因潜在特征分布漂移导致的身份漂移与语义质量退化**，以及由此带来的生成效率低下问题。

### 1. 音频注入：从“拼接”到“原生注意力融合”

现有方法通常将音频条件作为外挂模块处理，而 Soul 选择在 DiT 架构内部新增 **Audio-Attention 层**。该层并非从零训练，而是以原始文本注意力权重初始化，输入为 Whisper 预提取的音频特征。这一设计使得音频信号能够以与文本对等的方式参与去噪过程，驱动唇形与表情生成，避免了外挂式注入带来的模态对齐损失。

### 2. 长时生成：码本约束下的分布抗漂移机制

这是 Soul 最具原创性的贡献。长时视频生成的核心难点在于：随着时间推进，潜在特征逐渐偏离训练分布，导致颜色偏移、细节丢失等退化现象。Soul 的解决方案是一个**阈值感知码本替换**策略，其运作机制分为两步：

1. **码本构建**：利用 Soul-1M 训练数据中所有样本的潜在特征，通过 K-Means 聚类形成离散码本，每个码本中心代表一种“正常”的特征模式。
2. **推理校正**：在长时生成过程中，对每一帧的潜在特征计算其与码本中心的距离；当偏离超过预设阈值时，强制将其替换为最近的码本中心，从而将特征约束回训练分布附近。

配合**关键帧复制**（将首帧作为身份/背景/风格锚点复制到每个片段开头）与**片段间潜在帧重叠**（默认 2 帧），该机制在保持身份与场景一致性的同时，避免了突变伪影。消融实验（图 7）直观展示了关闭码本替换后随时间出现的颜色偏移与细节丢失，证实了其作为因果调节变量的有效性。

### 3. 推理效率：步数-CFG 联合蒸馏与轻量化解码器

Soul 将推理效率优化视为系统可用性的必要条件。两项关键改造：

- **步数与 CFG 联合蒸馏**：同时减少采样步数并移除 Classifier-Free Guidance，在保持生成质量的前提下实现 7.5× 加速。
- **eVAE-Wan2.2-5B-35M 解码器**：将官方 Wan2.2-5B VAE 解码器的参数从 550.05M 压缩至 34.97M，MACs 从 688.58T 降至 43.34T。

两项叠加后，总体加速比达到 **11.4×**（单 GPU，109×1088×1920 分辨率下从约 1020 秒降至 89.4 秒），而性能退化极小：Video-Text Consistence 仅从 4.85 降至 4.83，LSE-D 从 0.130 微增至 0.144（表 3）。

### 方法谱系与知识库定位

Soul 处于**音频驱动数字人动画**与**长时视频生成**的交叉点。相较于同类工作：

- 相比 **Sonic**（Ji et al., CVPR 2025）等仅聚焦音频-唇形同步的方法，Soul 引入了文本-音频联合条件与长时一致性约束。
- 相比 **StableAvatar**（Tu et al., arXiv 2025）等支持无限时长的方法，Soul 的码本替换机制提供了更显式的分布约束，而非依赖隐式的时序正则。
- 相比 **EchoMimicV3**（Meng et al., arXiv 2025）等统一多模态方案，Soul 在效率优化上更为激进，通过蒸馏与轻量化解码器实现了实用级推理速度。
- 与商用产品 **HeyGen**、**Kling-Avatar** 的主观对比（表 4）显示，Soul 在整体自然度、身份一致性、文本一致性和音视频同步四个维度上均取得领先。

### 局限与待验证方向

1. **复杂动作泛化**：对于剧烈全身动作（快速旋转、多人交互），仍可能出现伪影或肢体不自然，需要手动验证极端场景下的表现。
2. **数据覆盖**：Soul-1M 主要覆盖常见动作，稀有动作类型与跨语种音频的支持有限。
3. **阈值自适应**：当前码本替换阈值需预设，能否在无训练条件下自适应调节以适应不同生成场景，仍为开放问题。
4. **评估偏差**：Soul-Bench 为 AI 生成数据，其统计分布可能与真实视频存在偏差，导致某些指标的绝对数值（如 LSE-C、Audio-Video Alignment）超出真实视频上限，跨方法对比时需注意这一偏差。



Soul 的整体框架围绕一个核心瓶颈构建：**长时多模态数字人动画中的潜在特征分布漂移（latent feature shift）**，这会导致身份漂移、颜色偏移和细节丢失。为此，Soul 设计了一条从数据构建、模型注入到高效推理的完整流水线，其因果调节旋钮是**基于聚类码本的阈值感知替换策略（threshold-aware codebook replacement）**，在生成过程中将偏离分布的潜在特征约束回训练分布附近，从而抑制时序退化。

### 流水线总览

Soul 的框架可分为四个紧密耦合的模块阶段，如图 2 所示。

**1. 基础视频生成模型**
Soul 以 **Wan2.2-5B** 作为骨干视频生成模型。该模型原生仅支持文本条件，不支持音频输入，因此需要额外的模态注入机制。

**2. 音频注入（Audio-Attention Injection）**
为驱动唇形与表情，Soul 在 Wan2.2-5B 的 DiT 块中新增 **Audio-Attention 层**。具体而言：
- 音频特征由 **Whisper** 预提取。
- 新增的 Audio-Attention 层使用原始文本注意力权重进行初始化，以加速收敛并保持语义空间的对齐。
- 这一设计使音频信号能够自然地融入文本驱动的生成过程，驱动唇形与面部动画。

**3. 长时生成策略**
为实现跨片段一致的长时动画，Soul 引入了三重机制：
- **关键帧条件（Pivotal Frame Conditioning）**：将首帧作为身份、背景和风格的“关键表示”，复制到每个生成片段的开头，确保全局一致性。
- **片段间潜在重叠（Intra-clip Overlap）**：在潜在空间中，将前一片段的末尾帧（默认 2 帧）复制到当前片段的开头，提升时序连贯性。
- **阈值感知码本替换（Threshold-aware Codebook Replacement）**：这是框架的核心创新。Soul 利用训练集 **Soul-1M** 中所有样本的潜在特征，通过 K-Means 聚类构建离散码本。推理时，对每个生成帧的潜在特征进行码本查询，若其与最近聚类中心的距离超过预设阈值，则用聚类中心替换该特征。这相当于一种“柔性校正”，将离群特征拉回训练分布，从而有效抑制长时生成中的颜色偏移和细节退化（图 7）。

**4. 高效推理部署**
Soul 通过两项关键优化实现 **11.4× 推理加速**：
- **步数/CFG 联合蒸馏（Step/CFG Distillation）**：同时减少采样步数并移除无分类器引导（CFG），带来约 7.5× 加速。
- **轻量化解码器 eVAE-Wan2.2-5B-35M**：将官方 Wan2.2-5B VAE 解码器参数从 555.05M 降至 34.97M，MACs 从 688.58T 降至 43.34T，进一步压缩解码延迟。

### 输入输出流

- **输入**：一段参考图像（提供身份与背景）、一段文本描述（驱动场景与动作语义）、一段音频（驱动唇形与表情）。
- **处理**：参考图像被编码为潜在表示，文本与音频分别通过文本编码器和 Whisper 提取特征，注入 DiT 去噪过程。长时生成通过滑动窗口方式逐片段生成，片段间通过关键帧复制、潜在重叠和码本替换维持一致性。
- **输出**：一段高保真、身份一致、语义对齐的长时数字人视频，默认分辨率为 109×1088×1920，最长可达 4 分钟。

### 关键模块关系

码本替换模块与长时生成策略形成互补：潜在重叠保证了片段间的平滑过渡，而码本替换则防止了随生成时间累积的分布漂移。蒸馏与轻量 VAE 则在不显著牺牲质量的前提下，使上述复杂流水线能够在单 GPU 上以可接受的延迟运行。

### 补充图表

![[assets/figures/papers/paper_list_l1079_https_arxiv_org_abs_2512_13495/figures/002_Figure_2.jpg]]
*Figure 2: Overview of Soul for semantic-consistent and long-term multimodal-driven human video animation*



Soul 系统围绕“长时多模态人类视频动画”这一目标，在 Wan2.2-5B 基座模型上引入了四个关键模块，分别解决音频注入、长时一致性、推理效率三个核心问题。

### Audio-Attention 音频注入

Soul 在 Wan2.2-5B 的 DiT 块中新增 Audio-Attention 层，用于接收 Whisper 预提取的音频特征。该模块的权重直接从原始文本注意力权重初始化，使模型在微调初期即具备合理的跨模态映射能力，从而驱动唇形与表情生成。

### 长时生成一致性策略

长时推理的核心瓶颈在于潜在特征分布随生成步数累积而发生漂移，导致身份漂移、颜色偏移和细节丢失。Soul 通过三级机制协同抑制这一退化：

1. **Pivotal Frame Conditioning（关键帧条件）**：将首帧视为身份、背景和风格的“锚点”，在生成每个片段时将其复制到片段开头，提供稳定的视觉参考。
2. **Intra-clip Overlap（片段间潜在帧重叠）**：在潜在空间中，将前一片段末尾的 2 帧复制到当前片段开头，提升片段间的时序连贯性。
3. **Threshold-aware Codebook Replacement（阈值感知码本替换）**：这是 Soul 最具创新性的模块。具体做法是：从 Soul-1M 训练集中预提取所有样本的潜在特征，使用 K-Means 聚类构建离散码本。推理时，对每一步生成的潜在特征进行最近邻检索，当特征与码本中心的距离超过预设阈值时，将其替换为码本中心向量，从而将偏离分布的离群特征“拉回”训练分布附近。该机制在保持身份与场景一致性的同时，避免了硬性替换带来的突变伪影。

### 推理效率优化

Soul 采用两步蒸馏策略实现 11.4× 加速：

- **Step / CFG 联合蒸馏**：同时减少 DDIM 采样步数并去除 Classifier-Free Guidance，消除 CFG 的双重前向推理开销，单独贡献 7.5× 加速。
- **eVAE-Wan2.2-5B-35M 轻量化解码器**：将官方 VAE 解码器参数量从 555.05M 压缩至 34.97M，MACs 从 688.58T 降至 43.34T，在性能几乎无损的前提下进一步降低推理延迟。

### 公式说明

本文未提供独立的理论公式推导。核心机制——阈值感知码本替换——可形式化为：

设码本为 $\mathcal{C} = \{c_1, c_2, \ldots, c_K\}$，其中 $c_k$ 为第 $k$ 个聚类中心。对于生成过程中第 $t$ 步的潜在特征 $z_t$，其替换规则为：

$$
z_t' = \begin{cases}
c_{k^*} & \text{if } \|z_t - c_{k^*}\|_2 > \tau \\
z_t & \text{otherwise}
\end{cases}
$$

其中 $k^* = \arg\min_k \|z_t - c_k\|_2$ 为最近邻码本索引，$\tau$ 为预设的距离阈值。该公式描述了离群特征被柔性校正的过程，但原文未显式给出此公式，系根据方法描述重构。

> **注意**：上述公式为基于方法描述的逻辑重构，非原文直接提供。如需精确形式化定义，建议查阅原文或代码实现。

### 补充图表

![[assets/figures/papers/paper_list_l1079_https_arxiv_org_abs_2512_13495/figures/010_Figure_7.jpg]]
*Figure 7: Over time, the approach without using the threshold-aware codebook is prone to color deviation and loss of details. The data is derived from the AI-generated Soul-Bench*



## 实验与关键发现

### 核心指标与多维度对比

Soul 在自建基准 **Soul-Bench** 上与一系列代表性方法进行了全面对比，包括音频驱动肖像动画方法 **Sonic** (Ji et al., CVPR 2025)、文生视频说话人适配方法 **Wan-S2V**、稀疏帧视频配音方法 **InfiniteTalk**、无限时长音频驱动化身方法 **StableAvatar** (Tu et al., arXiv 2025)、统一多模态动画方法 **EchoMimicV3** (Meng et al., arXiv 2025)、DiT 架构肖像动画方法 **Hallo3** (Cui et al., CVPR 2025)，以及近期开源方案 **OmniAvatar** 与商用产品 **HeyGen**、**Kling-Avatar**。

定量结果（Table 2）显示，Soul 在六个维度上取得最优或次优成绩：

![[assets/figures/papers/paper_list_l1079_https_arxiv_org_abs_2512_13495/figures/007_Table_2.jpg]]
*Table 2: Quantitative results with SoTAs on Soul-Bench. Bold / underline / wavy line for optimal / suboptimal / third-optimal metrics. For reference: LSE-C is 6.12 (training dataset) and Audio-Video Alignment is 23.19 (real videos) [85]. Values exceeding these thresholds lack significant distinguishability. Our Soul comprehensively achieves significantly the best result*

- **视频-文本一致性 (Video-Text Consistence↑)**：Soul 得分 4.85，超过 StableAvatar 的 4.77。
- **唇同步精度 (LSE-D↓)**：Soul 的 0.130 大幅领先 Sonic 的 0.663，降幅达 0.533。
- **唇同步置信度 (LSE-C↑)**：Soul 的 6.82 低于 InfiniteTalk 的 8.48，但需注意该指标在训练集上参考值为 6.12，超过此阈值后区分度有限。
- **身份一致性 (Identity Consistence↑)**：Soul 的 0.763 略高于 Wan-S2V 的 0.750。
- **视频质量 (Video Quality↑)**：Soul 的 72.60 超越 StableAvatar 的 71.40。
- **音视频对齐 (Audio-Video Alignment↑)**：Soul 的 0.255 低于 Wan-S2V 的 0.330，但真实视频参考值为 23.19，此区间内数值差异的感知意义不大。

需要指出，Soul-Bench 数据由 T2V 模型生成，其统计分布与真实视频存在偏差，可能导致 LSE-C 和 Audio-Video Alignment 等指标的绝对值超出真实视频上限。跨方法对比时，相对排序比绝对数值更具参考价值。

### 长时生成中的退化抑制

长时推理的核心瓶颈在于潜在特征分布随生成进程发生漂移，导致颜色偏移和细节丢失。Soul 提出的**阈值感知码本替换 (Threshold-aware Codebook Replacement)** 策略正是针对这一退化机制设计：利用 Soul-1M 训练数据的潜在特征通过 K-Means 聚类构建离散码本，在长时生成过程中，对偏离分布的离群特征按阈值约束回码本中心附近，从而将生成分布“拉回”训练分布邻域。

消融可视化（Figure 7）直观展示了该策略的效果：不使用码本替换时，即使存在片段间潜在帧重叠，生成视频仍随时间推移出现明显颜色偏差和纹理退化；引入阈值感知码本替换后，长时生成的身份一致性和场景稳定性得到有效保持。Soul 最终可生成最长 4 分钟的身份一致视频（Figure 6 顶部），验证了该策略对时序退化的抑制能力。

![[assets/figures/papers/paper_list_l1079_https_arxiv_org_abs_2512_13495/figures/008_Figure_6.jpg]]
*Figure 6: Top: Identity-consistent long-term animation across varying scenes with text and audio conditioning of our Soul. Bottom: Diverse generative capabilities for practical applications of Soul with samples from Soul-Bench*

### 推理效率的系统性优化

Soul 通过三个递进层次的优化实现 11.4× 推理加速（Table 3），且性能损失极小：

![[assets/figures/papers/paper_list_l1079_https_arxiv_org_abs_2512_13495/figures/009_Table_3.jpg]]
*Table 3: Impact of different acceleration components on efficiency and performance. Defalut 129×1088×1920 resolution on one GPU. Speedup is relative to the Baseline of the first line. FA2: FlashAttention2; KD: Step and CFG Knowledgement Distillation; eVAE: Our designed efficient eVAE-Wan2.2-5B-35M*

1. **FlashAttention2 (FA2)**：基础注意力加速，带来约 1.2× 提升。
2. **步数与 CFG 联合蒸馏 (KD)**：同时减少采样步数并移除无分类器引导，在 Video-Text Consistence 仅从 4.85 降至 4.83、LSE-D 从 0.130 升至 0.144 的代价下，实现 7.5× 加速。
3. **轻量化解码器 eVAE-Wan2.2-5B-35M**：将原 VAE 解码器参数量从 555.05M 压缩至 34.97M，MACs 从 688.58T 降至 43.34T（Table 1），最终单 GPU 推理 109×1088×1920 分辨率视频的时延从约 1020 s 降至 89.4 s，总加速 11.4×。

![[assets/figures/papers/paper_list_l1079_https_arxiv_org_abs_2512_13495/figures/003_Table_1.jpg]]
*Table 1: Efficiency and performance of efficient eVAE over official Wan2.2-5B-VAE. Defalut 720×1280 resolution on one GPU*

### 与商用产品的主观对比

人工评审（Table 4）将 Soul 与商用产品 HeyGen 和 Kling-Avatar 在四个维度进行对比：整体自然度 (4.17)、身份一致性 (4.00)、文本一致性 (4.11)、音视频同步 (4.20)。Soul 在所有维度上均取得最高评分，表明其在主观感知质量上已具备与商业方案竞争的能力。

![[assets/figures/papers/paper_list_l1079_https_arxiv_org_abs_2512_13495/figures/011_Table_4.jpg]]
*Table 4: Human study with commercial products. ➀ Overall Naturalness, ➁ ID Consistency, ➂ Text Consistency, and ➃ Audio-Visual Synchronization*

### 已知局限与失效模式

尽管 Soul 在长时多模态动画上表现突出，仍存在以下局限：

- **复杂全身动作**：对于快速旋转、多人交互等剧烈运动，可能出现肢体伪影或不自然形变。当前方法缺乏 3D 几何先验来约束身体结构的空间一致性。
- **数据覆盖偏差**：Soul-1M 主要覆盖常见动作类型，对稀有动作和跨语种音频的支持有限，可能影响对应场景下的泛化质量。
- **评估基准偏差**：Soul-Bench 为 AI 生成数据，其评估分数可能无法完全反映真实场景表现，部分指标（如 LSE-C）已接近或超过训练集参考值，区分度下降。

### 补充图表

![[assets/figures/papers/paper_list_l1079_https_arxiv_org_abs_2512_13495/figures/006_Figure_5.jpg]]
*Figure 5: Qualitative comparison with state-of-the-arts on Soul-Bench. The timings are based on an average generation duration of 30s. Our Soul can achieve strong semantic consistency and multi-scene generalization while preserving generation quality, with higher efficiency. The data is derived from the AI-generated Soul-Bench*

![[assets/figures/papers/paper_list_l1079_https_arxiv_org_abs_2512_13495/figures/004_Figure_3.jpg]]
*Figure 3: Statistical distributions of our Soul-1M from different perspectives*

![[assets/figures/papers/paper_list_l1079_https_arxiv_org_abs_2512_13495/figures/005_Figure_4.jpg]]
*Figure 4: Statistical distributions of Soul-Bench*



## 定位与知识库关联

### 1. 与现有方法的谱系关系

Soul 处于**音频驱动数字人动画**这一快速演进的技术脉络中，其设计同时回应了多模态条件生成、长时一致性保持和推理效率三个维度的挑战。以下从基座模型选择、音频注入机制和长时生成策略三个关键维度定位其与现有工作的关系。

**基座模型选择：从专用架构到通用视频生成模型。** 早期工作如 **Sonic**（Ji et al., CVPR 2025）和 **Hallo3**（Cui et al., CVPR 2025）多采用针对肖像动画专门设计的 DiT 架构，而 Soul 直接构建在通用文生视频模型 **Wan2.2-5B** 之上。这一选择使其天然继承了 Wan2.2-5B 在文本语义理解和场景多样性上的能力，但也引入了原生不支持音频条件的约束，迫使 Soul 设计专门的音频注入机制来弥补模态缺口。

**音频注入方式：从替换式到增量式注意力融合。** 与部分方法将音频特征直接拼接到文本嵌入或替换文本条件不同，Soul 在 DiT 块中**新增 Audio-Attention 层**，并用文本注意力权重初始化该层。这一增量式设计的关键在于：它保留了原有文本注意力通路，使模型可以同时响应文本和音频两个模态的驱动信号，从而支持“文本描述场景 + 音频驱动唇形/表情”的联合控制范式。相比之下，**EchoMimicV3**（Meng et al., arXiv 2025）虽然也追求多模态统一，但其具体注入方式与 Soul 的增量注意力机制存在架构层面的差异。

**长时生成策略：从单片段独立到码本约束的跨片段一致性。** 这是 Soul 最具区分度的技术贡献。多数现有方法（如 **Wan-S2V**、**InfiniteTalk**）以单片段为生成单元，片段间缺乏显式的一致性约束，导致长时推理中出现身份漂移和视觉退化。**StableAvatar**（Tu et al., arXiv 2025）虽声称支持无限时长，但其一致性机制与 Soul 的码本替换策略有本质不同。Soul 的**阈值感知码本替换（threshold-aware codebook replacement）**通过以下机制实现跨片段约束：

1. 从训练集 Soul-1M 的潜在特征中通过 K-Means 聚类构建离散码本；
2. 推理时对每个生成帧的潜在特征进行最近邻检索；
3. 仅当特征与码本中心的距离超过预设阈值时才执行替换，将离群特征“拉回”训练分布附近。

这种“柔性校正”策略的核心优势在于：它既抑制了长时推理中的分布漂移（表现为颜色偏移和细节丢失，见 Figure 7），又避免了强制替换可能引入的突变伪影。从方法论角度看，该策略可视为一种**推理时分布正则化**，与训练阶段的分布约束（如 VAE 的 KL 散度）形成互补。

**效率优化：从单一加速到多组件联合蒸馏。** Soul 的 11.4× 加速并非依赖单一技术，而是**步数/CFG 联合蒸馏 + 轻量化 eVAE 解码器**的协同结果。其中 eVAE-Wan2.2-5B-35M 将解码器参数量从 555.05M 压缩至 34.97M（约 16×），MACs 从 688.58T 降至 43.34T，这一压缩比在同类工作中较为突出。Table 3 的消融表明，仅步数/CFG 蒸馏贡献 7.5× 加速，eVAE 在此基础上进一步贡献约 1.5×，且性能下降极小（Video-Text Consistence 从 4.85 降至 4.83，LSE-D 从 0.130 升至 0.144）。

### 2. 适用边界与局限

**适用场景。** Soul 在以下条件下表现最优：（1）音频驱动的半身/肖像数字人动画，动作幅度适中；（2）文本描述的场景与音频内容语义一致；（3）需要长时（分钟级）身份保持的生成任务。Figure 6 顶部展示了最长 4 分钟的身份一致视频生成能力，Table 2 显示其在 Soul-Bench 的六个指标上全面领先现有开源方案。

**已知局限。** 论文明确指出了三方面局限：

- **复杂动作退化**：对于剧烈、复杂的全身动作（如快速旋转、多人交互），仍可能出现伪影或肢体不自然。这源于训练数据 Soul-1M 主要覆盖常见动作类型，且 Wan2.2-5B 基座本身对极端人体姿态的建模能力有限。
- **数据覆盖偏差**：Soul-1M 在稀有动作类型和跨语种音频上的覆盖不足，可能限制模型在这些场景下的泛化能力。
- **评估基准偏差**：Soul-Bench 由 T2V 模型生成，其统计分布可能与真实世界视频存在偏差。Table 2 的备注明确指出，LSE-C 的训练集上限为 6.12、Audio-Video Alignment 的真实视频上限为 23.19，超出这些阈值的分数缺乏显著区分度——Soul 的 Audio-Video Alignment（0.255）和部分基线的 LSE-C 值即受此影响，跨方法对比时需注意这一系统性偏差。

### 3. 开放问题

从 Soul 的设计边界向外延伸，以下问题值得进一步探索：

1. **3D 几何先验的融合**：当前 Soul 完全在 2D 潜在空间中操作，缺乏对 3D 人体结构的显式建模。若能融入 3DMM 等几何先验，有望提升全身动作的自然度和空间一致性，尤其是在遮挡和旋转场景下。

2. **数据覆盖的扩展路径**：如何低成本地扩展 Soul-1M 以覆盖更多稀有动作类型和跨语种音频？合成数据增强（如利用 T2V 模型生成特定动作片段）可能是一条可行路径，但需注意合成数据与真实数据之间的分布差异。

3. **自适应阈值机制**：当前码本替换的阈值是预设的固定值。能否设计无训练的自适应阈值调节策略，使模型根据生成场景的复杂度（如静态背景 vs. 动态背景）动态调整替换强度？这将提升方法在不同场景下的鲁棒性。

4. **与商用产品的差距**：Table 4 的人审结果显示 Soul 在整体自然度（4.17 vs. HeyGen 4.25）和身份一致性（4.00 vs. HeyGen 4.20）上仍略逊于商用产品 **HeyGen**，表明在极致真实感和细节保真度上仍有提升空间。



## 原文 PDF

![[paperPDFs/CVPR_2026/Soul_Breathe_Life_into_Digital_Human_for_High_fidelity_Long_term_Multimodal_Animation.pdf]]

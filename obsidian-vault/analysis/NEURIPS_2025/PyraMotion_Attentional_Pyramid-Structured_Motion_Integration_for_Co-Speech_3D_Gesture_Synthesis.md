---
title: "PyraMotion: Attentional Pyramid-Structured Motion Integration for Co-Speech 3D Gesture Synthesis"
type: paper
paper_level: A
venue: NEURIPS
year: 2025
pdf_ref: paperPDFs/NEURIPS_2025/PyraMotion_Attentional_Pyramid-Structured_Motion_Integration_for_Co-Speech_3D_Gesture_Synthesis.pdf
project_link: null
code_link: "https://github.com/Williamy946/PyraMotion"
aliases:
- PAVPTP
- PyraMotion
tags:
- NEURIPS_2025
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 多尺度金字塔运动表示与注意力融合（APVQ-VAE + 金字塔Token预测器），使模型能够自适应地利用不同时间粒度的运动token。
primary_logic: 借鉴计算机视觉特征金字塔思想，构建从粗到细的多尺度运动表征，通过共享码本和注意力机制让不同身体部位自主关注适合的时间尺度，显著提升全身手势生成的多样性和自然度。
claims:
- PyraMotion在BEAT2数据集上全面超越现有最强方法（FGD、MSE、LVD等指标最优）
- 消融实验表明移除TransTCN解码器导致生成质量大幅下降（FGD从4.612升至6.178），证明注意力残差融合的设计至关重要
- APVQ-VAE在重建任务上显著优于普通VQ-VAE，各身体部位关节旋转均方根误差更低，FGD 1.296 vs 普通VQ-VAE的更高值
- 注意力图显示不同身体部位呈现显著的时间尺度偏好（面部偏好细粒度，下半身偏好粗粒度），验证了金字塔多尺度表示的合理性
---

# PyraMotion: Attentional Pyramid-Structured Motion Integration for Co-Speech 3D Gesture Synthesis

> [!tip] 核心洞察
> 借鉴计算机视觉特征金字塔思想，构建从粗到细的多尺度运动表征，通过共享码本和注意力机制让不同身体部位自主关注适合的时间尺度，显著提升全身手势生成的多样性和自然度。

| 字段 | 内容 |
|------|------|
| 中文题名 | PyraMotion: 面向语音同步3D手势合成的注意力金字塔结构运动集成 |
| 英文题名 | PyraMotion: Attentional Pyramid-Structured Motion Integration for Co-Speech 3D Gesture Synthesis |
| 会议/期刊 | NEURIPS 2025 |
| Links | [paper](https://proceedings.neurips.cc/paper_files/paper/2025/hash/ca6403397d60b7dbf9c7158a1c19094a-Abstract-Conference.html) · [Code](https://github.com/Williamy946/PyraMotion) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | PyraMotion (APVQ-VAE + Pyramidal Token Predictor) |
| Dataset | BEAT2 |

> [!tip] 效果简介
> - BEAT2 上，FGD (↓) 4.612；MSE (↓) 7.176 ± 0.028；LVD (↓) 7.270 ± 0.011。

## 概要

语音同步3D手势生成的核心瓶颈在于：现有VQ-VAE方法将动作编码为固定帧数的离散token，无法同时捕捉不同身体部位在多个时间尺度上的运动模式——面部表情变化迅速而精细，下半身运动则相对缓慢且粗粒度，单一尺度表征必然牺牲部分身体部位的表现力。

PyraMotion针对这一瓶颈，提出**注意力金字塔运动集成框架**，核心思路借鉴计算机视觉中的特征金字塔思想，构建从粗到细的多尺度运动表征，并通过共享码本与注意力机制让不同身体部位自主关注适合的时间尺度。具体而言，框架包含两个阶段：（1）**APVQ-VAE**（Attentional Pyramidal VQ-VAE）使用多个不同时间尺度的TCN编码器将手势序列编码为金字塔式token序列，经共享码本量化后，通过带注意力残差融合的TransTCN解码器重建运动；（2）**金字塔Token预测器**从音频和文本特征出发，以从粗到细的迭代方式预测多尺度运动token，最终由APVQ-VAE解码器生成全身3D手势。

在BEAT2数据集上，PyraMotion全面超越现有最强方法，关键指标FGD降至**4.612**，MSE为**7.176**，LVD为**7.270**（Table 1）。消融实验表明，TransTCN解码器的注意力残差融合设计对生成质量至关重要——移除后FGD从4.612升至6.178（Table 2）；APVQ-VAE在重建任务上显著优于普通VQ-VAE（FGD 1.296 vs 更高值，Table 3）。注意力图可视化进一步揭示面部偏好细粒度token、下半身偏好粗粒度token的时间尺度分工模式（Figure 3），验证了金字塔多尺度表征的合理性。

方法定位上，PyraMotion属于**离散表征+自回归预测**范式的语音驱动手势生成方法，与EMAGE（Yi et al., CVPR 2023）、CaMN（Liu et al., CVPR 2024）等同期工作相比，核心差异在于将单尺度VQ-VAE扩展为多尺度金字塔结构，使运动表征能够覆盖不同身体部位的时间动态范围。当前局限包括：金字塔层数需手动选择，推理时间约41秒（长于EMAGE的约22秒），且尚未支持多模态条件控制。



语音驱动的3D手势合成旨在从语音音频中生成与语音节奏和语义协调的自然手势动作，是虚拟人交互、数字人等应用中的核心技术。近年来，随着大规模多模态数据集的构建和深度生成模型的发展，该领域取得了显著进展。现有方法大致可分为两类：基于回归的方法直接学习语音到手部动作的映射，而基于生成模型的方法则利用VAE、扩散模型或VQ-VAE等框架对动作分布进行建模，以提升生成手势的多样性和表现力。

### 核心瓶颈：固定时间尺度的运动编码

当前主流方法中，VQ-VAE已成为手势合成的重要基础架构。其核心思路是将连续的手势动作序列编码为离散的token，再通过自回归或掩码预测的方式从语音条件生成token序列，最终解码为动作。然而，**现有VQ-VAE方法普遍采用固定帧数（单一时间尺度）对运动进行编码**，这一设计存在根本性局限。

人体手势动作天然具有多时间尺度的特性：面部表情（如眉毛挑动、嘴角微动）往往在短时间窗口内完成，而下半身动作（如重心转移、步伐调整）则跨越较长的时间跨度。图1直观展示了这一现象——不同持续时间的表现型运动模式共存于同一手势序列中。固定尺度的编码方式迫使模型在同一时间粒度上处理所有身体部位的运动，无法同时捕捉快速变化的精细表情和缓慢演变的全身姿态，导致生成手势的表现力受限，尤其在全身手势合成场景中更为突出。

### 现有方法的缺口

尽管已有工作尝试通过分部位建模来缓解这一问题——例如**EMAGE**（Yi et al., CVPR 2023）和**CaMN**（Liu et al., CVPR 2024）分别对面部、手部和身体进行独立处理——但这些方法仍然在单一时间尺度上对每个部位进行编码，未能从根本上解决多尺度运动模式的学习问题。其他代表性方法如**TalkSHOW**（Yoon et al., TOG 2020）、**DiffuseStyleGesture**（Yang et al., arXiv 2023）和**Gesture2Vec**（Yazdian et al., IROS 2022）同样缺乏对时间尺度多样性的显式建模。

### 核心洞察与本文动机

本文的核心洞察源自计算机视觉中**特征金字塔**（Feature Pyramid）的思想：通过构建从粗到细的多尺度表征，使模型能够同时捕捉不同粒度的信息。将这一思想迁移到运动生成领域，可以自然地解决上述瓶颈——**让不同身体部位自主关注适合自身运动模式的时间尺度**，而非被强制统一编码。

基于这一洞察，本文提出**PyraMotion**框架，核心包含两个创新设计：

1. **注意力金字塔VQ-VAE（APVQ-VAE）**：使用多个不同时间尺度的TCN编码器对运动序列进行并行编码，产生多尺度嵌入序列，并共享一个离散码本进行矢量量化。解码时，通过注意力机制自适应地融合不同尺度的token，使各身体部位能够从最相关的时间粒度中获取信息。

2. **金字塔Token预测器**：从粗到细逐层预测运动token，结合音频节奏特征和文本语义特征，为不同身体部位生成对应的多尺度token序列。

通过这一设计，PyraMotion从根本上改变了运动编码的范式——从“固定尺度统一编码”转向“多尺度自适应融合”，为全身手势生成的多样性和自然度提升提供了新的技术路径。



## 核心方法与创新机理

PyraMotion 的核心创新在于将计算机视觉中的**特征金字塔思想**引入语音同步手势生成，构建了从粗到细的多尺度运动表征与注意力融合机制，从而解决了现有 VQ-VAE 方法以固定帧数编码运动、无法同时捕捉不同身体部位在不同时间尺度上运动模式的瓶颈。

具体而言，PyraMotion 在以下四个关键维度上对 baseline 进行了系统性改造：

| 设计维度 | Baseline 做法 | PyraMotion 创新 | 证据锚点 |
|---------|-------------|---------------|---------|
| 运动编码的时间尺度 | 固定帧数（单尺度）编码 | 多尺度金字塔编码：使用 $n$ 个 TCN，帧数按 $2^i$ 递减，产生不同时间粒度的嵌入序列 | Eq.2 |
| VQ-VAE 解码器结构 | 单 TCN 解码器 | Transpose TCN + 注意力残差融合：将多层重建结果堆叠后通过注意力计算残差，与均值直接重建结果相加 | Eq.4 |
| 身体部位建模方式 | 统一建模全身运动 | 分四个部位（面部、上半身、手、下半身）独立提取特征并融合，允许各部位自主关注适合的时间尺度 | Eq.8, Sec 3.4 |
| Token 预测器的粒度 | 单尺度自回归预测 | 粗到细的多尺度迭代预测，结合音频、文本和部位掩码信息 | Eq.13 |

### 多尺度运动编码与共享码本

APVQ-VAE 使用 $n$ 个具有不同时间感受野的 TCN 网络对原始手势序列 $\mathbf{g}$ 进行编码：

$$\mathbf{F} = [\mathbf{f}_1, ..., \mathbf{f}_n] = \mathcal{E}(\mathbf{g}) = [\mathbf{TCN}_1(\mathbf{g}), ..., \mathbf{TCN}_n(\mathbf{g})]$$

所有尺度的嵌入序列共享同一个码本 $Z$，以确保嵌入语义的一致性。量化后通过查找操作得到 $\hat{\mathbf{F}}$，再由解码器重建手势。为缓解不同核大小带来的尺度差异，卷积输出除以核大小进行归一化（Eq.5），提升训练稳定性。

### 注意力残差解码

解码器的关键设计是将 TransTCN 输出的多层重建结果堆叠为 $\hat{\mathbf{F}}_{stack}$，通过注意力机制计算残差并与均值重建结果相加：

$$\hat{\mathbf{g}} = \mathcal{D}(\hat{\mathbf{F}}) = \mathrm{Attention}(\mathrm{Mean}(\hat{\mathbf{F}}_{stack}), \hat{\mathbf{F}}_{stack}, \hat{\mathbf{F}}_{stack}) + \mathbf{Mean}(\hat{\mathbf{F}}_{stack})$$

消融实验（Table 2）为此设计提供了强有力的证据：将 TransTCN 替换为普通 TCN（w/o TransTCN）后，FGD 从 4.612 升至 6.178，BC 升至 7.132，Diversity 降至 12.869，MSE 升至 8.833，LVD 升至 9.511——生成质量出现全面且大幅的下降，证明注意力残差融合是模型性能的关键支撑。

### 部位感知的多尺度表征

PyraMotion 将全身运动分解为面部、上半身、手、下半身四个部位，分别生成隐含表示（Eq.8）。身体部位利用掩码手势提示（前 8 帧真值）与 TCAT 进行融合，捕捉各部位间的互信息。在此基础上，通过连续帧均值池化和与 APVQ-VAE 同构的 TCN 网络构建两种金字塔表征——平均化金字塔和 TCN 金字塔（Eq.9），并由 Temporal Cross-Attention Transformer 捕捉二者的相关性（Eq.10）。

注意力图可视化（Figure 3）直接验证了该设计的合理性：**面部偏好细粒度时间尺度，下半身偏好粗粒度时间尺度**，不同身体部位呈现出显著的时间尺度偏好差异。这一发现从机制层面解释了为什么单尺度编码无法充分捕捉全身手势的表现力。

### 粗到细的迭代 Token 预测

Pyramidal Token Predictor 从最粗尺度开始，逐层结合上一层的预测 token 与当前层隐含特征进行 token 分布预测：

$$\hat{\mathbf{q}}_i^{parts} = \mathrm{MLP}(\tilde{\mathbf{h}}_i^{parts} + \hat{\mathbf{q}}_{i+1}^{parts}), \quad i \in [0, n-2]$$

预测结果通过交叉熵损失（Eq.14）优化，使其逼近 APVQ-VAE 提取的真实 token 分布。这种粗到细的迭代预测策略使模型能够先确定运动的宏观结构，再逐步细化细节，与金字塔表征的多粒度特性形成闭环。

### 金字塔层数的选择

金字塔层数实验（Table 5）表明，4 层在重建与生成指标间取得最佳平衡；5 层引入过拟合，性能反而下降。这一发现说明**多尺度并非越多越好**——当前方法需要手动选择层数，尚无法根据数据集特性自适应调整，这是论文明确指出的一个局限性。



PyraMotion 采用两阶段训练范式，分别构建运动表征与生成控制。

**Stage 1：Attentional Pyramidal VQ-VAE (APVQ-VAE)。** 该阶段负责学习多尺度离散运动表征。给定全身3D手势序列 $\mathbf{\bar{g}} \in \mathbb{R}^{L \times (55 \times 6 + 100 + 4 + 3)}$（包含55个关节的6D旋转表示、100维面部表情参数、4个脚部接触标签和3维全局平移），APVQ-VAE通过 $n$ 个具有不同时间感受野的TCN编码器并行提取多尺度嵌入 $\mathbf{F} = [\mathbf{f}_1, ..., \mathbf{f}_n]$，所有尺度共享同一码本 $Z$ 进行矢量量化，确保嵌入语义一致性。解码端采用 TransTCN 与注意力残差融合机制，将量化后的多尺度 token 序列重建为原始手势。

**Stage 2：Pyramidal Token Predictor。** 该阶段冻结 APVQ-VAE 的解码器，训练一个从音频和文本预测多尺度运动 token 的生成器。输入音频 $\mathbf{a} \in \mathbb{R}^{L \cdot sf}$ 经特征提取后，通过注意力机制与文本内容特征融合，得到融合特征 $\mathbf{f}_{1:T}$。随后，模型分别为面部和身体部位生成隐含表示，并通过均值池化和与 Stage 1 同构的 TCN 网络构建两种金字塔表征。最终，从最粗尺度开始，逐层结合上一层的预测 token 与当前层隐含特征，以粗到细的方式迭代预测各部位的运动 token 分布，经 APVQ-VAE 解码器重建为手势序列。

**模块关系与数据流。** 两阶段之间通过共享码本和解码器实现紧耦合：Stage 1 提供的离散码本空间为 Stage 2 的 token 预测提供了可学习的量化目标；Stage 2 预测的 token 序列直接复用 Stage 1 训练好的解码器进行运动重建，避免了生成阶段对连续运动空间的直接回归。图2展示了完整的训练流程。

**关键设计决策。** 金字塔层数 $n$ 需手动设定（实验表明4层在重建与生成指标间取得最佳平衡，5层引入过拟合），模型尚不具备根据数据特性自适应调整层数的能力。

### 补充图表

![[assets/figures/papers/neurips_2025_pyramotion/figures/002_Figure_2.jpg]]
*Figure 2: The Overall Workflow of PyraMotion. Stage 1: APVQ-VAE learns the discrete latent representations of motions, denoted as tokens, and reconstructs the motion from the pyradical token series via decoder. Stage 2: The PyraMotion framework is trained to predict the pyradical token series of motion from audio and reconstruct the motion via decoder in APVQ-VAE*



PyraMotion 采用两阶段训练范式：第一阶段训练 **APVQ-VAE** 学习离散运动表征，第二阶段训练 **金字塔 Token 预测器** 从音频和文本中预测运动 token。以下聚焦两个阶段的核心模块及其关键公式。

### 第一阶段：APVQ-VAE

APVQ-VAE 的核心创新在于用多尺度金字塔编码替代传统 VQ-VAE 的单尺度编码，并通过注意力残差解码器实现跨尺度融合。

**多尺度编码。** 给定全身手势序列 $\mathbf{g}$，使用 $n$ 个不同时间尺度的 TCN 网络并行编码，产生多尺度嵌入序列：

$$\mathbf{F} = [\mathbf{f}_1, ..., \mathbf{f}_n] = \mathcal{E}(\mathbf{g}) = [\mathbf{TCN}_1(\mathbf{g}), ..., \mathbf{TCN}_n(\mathbf{g})]$$

其中 $\mathbf{f}_i$ 的帧数按 $2^i$ 递减，形成从细粒度到粗粒度的金字塔表征。所有尺度的嵌入共享同一个码本 $Z$，以保证嵌入语义的一致性。

**核归一化。** 为缓解不同 TCN 核大小带来的尺度差异，对卷积输出进行归一化：

$$\mathbf{r} = Conv(\mathbf{f}, ks, s, p) / ks$$

其中 $ks$ 为核大小，$s$ 为步长，$p$ 为填充。该操作将卷积输出除以核大小，提升训练稳定性。

**多尺度量化。** 对多尺度嵌入进行矢量量化，并通过共享码本 $Z$ 查找量化后的嵌入：

$$\mathbf{Q} = [\mathbf{q}_1, ..., \mathbf{q}_n] = \mathcal{Q}(\mathbf{F}), \quad \hat{\mathbf{F}} = \mathrm{lookup}(Z, \mathbf{Q})$$

**注意力残差解码器。** 解码器的关键设计是将 TransTCN 输出的多层重建结果堆叠，通过注意力机制计算残差，并与均值直接重建结果相加：

$$\hat{\mathbf{g}} = \mathcal{D}(\hat{\mathbf{F}}) = \mathrm{Attention}(\mathrm{Mean}(\hat{\mathbf{F}}_{stack}), \hat{\mathbf{F}}_{stack}, \hat{\mathbf{F}}_{stack}) + \mathbf{Mean}(\hat{\mathbf{F}}_{stack})$$

该设计的直觉是：均值重建提供基准信号，注意力残差补充跨尺度细节。消融实验（Table 2）证实，将 TransTCN 替换为普通 TCN 会导致 FGD 从 4.612 升至 6.178，生成质量大幅下降。

**损失函数。** APVQ-VAE 的优化目标为：

$$\mathcal{L}_{APVQ-VAE} = \mathcal{L}_{rec} + \mathcal{L}_{vel} + \mathcal{L}_{acc} + \beta \cdot \mathcal{L}_{commit}$$

其中 $\mathcal{L}_{rec}$ 为 Geodesic 重建损失，$\mathcal{L}_{vel}$ 和 $\mathcal{L}_{acc}$ 分别为速度和加速度的 L1 损失，$\mathcal{L}_{commit}$ 为码本承诺损失（权重 $\beta=1$），用于约束编码器输出接近码本向量。

### 第二阶段：金字塔 Token 预测器

预测器的目标是从音频和文本中预测 APVQ-VAE 提取的多尺度运动 token，采用从粗到细的迭代预测策略。

**音频-文本融合。** 通过元素级注意力系数融合节奏音频特征 $\mathbf{r}_{1:T}$ 和文本内容特征 $\mathbf{c}_{1:T}$：

$$\alpha = \mathrm{Softmax}(\mathrm{MLP}(\mathbf{r}_{1:T}, \mathbf{c}_{1:T}))$$

$$\mathbf{f}_{1:T} = \alpha \times \mathbf{r}_{1:T} + (1-\alpha) \times \mathbf{c}_{1:T}$$

**分部位隐含表示生成。** 分别为面部和身体部位生成隐含表示。面部表示由融合特征和面部位置编码拼接后经 MLP 得到；身体表示则结合掩码手势提示（前 8 帧真值）与 TCAT（Temporal Cross-Attention Transformer）进行融合：

$$\mathbf{h}^{face} = \mathrm{MLP}(\mathbf{f}^{face} \oplus \mathbf{p}_f)$$

$$\mathbf{h}^{body} = \mathbf{h}^{hints} + \mathrm{TCAT}(\mathbf{h}^{hints} \oplus \mathbf{p}_t, \mathbf{f}^{body})$$

其中 $\mathbf{h}^{hints} = \mathrm{SAN}(\bar{\mathbf{g}} + \mathbf{p}_t)$ 为掩码手势提示经自注意力网络处理后的表示。

**金字塔隐含表征构建。** 对部位隐含表示分别通过连续帧均值池化和与 APVQ-VAE 同构的 TCN 网络，构建两种金字塔表征：

$$\mathbf{H}_{mean}^{parts} = [\sigma(\mathbf{h}_{[0,...,2^i-1]}^{parts}), ...], \quad \mathbf{H}_{tcn}^{parts} = [\mathbf{TCN}_0(\mathbf{h}^{parts}), ...]$$

TCAT 用于捕捉这两种金字塔表征之间的相关性。

**粗到细 Token 预测。** 从最粗尺度开始，逐层结合上一层的预测 token 与当前层隐含特征进行 token 分布预测：

$$\hat{\mathbf{q}}_i^{parts} = \mathrm{MLP}(\tilde{\mathbf{h}}_i^{parts} + \hat{\mathbf{q}}_{i+1}^{parts}), \quad i \in [0, n-2]$$

该迭代机制使细粒度预测能够利用粗粒度已预测 token 的结构先验。

**分类损失。** 使用交叉熵损失优化各部位预测的 token 索引分布，使其逼近 APVQ-VAE 提取的真实 token：

$$\mathcal{L}_{cls}^{parts} = \mathrm{CrossEntropy}(\hat{\mathbf{Q}}^{parts}, \mathbf{Q}^{parts})$$

### 关键设计总结

| 模块 | 核心机制 | 关键公式 | 消融验证 |
|------|----------|----------|----------|
| 多尺度编码 | $n$ 个 TCN 并行编码，帧数按 $2^i$ 递减 | Eq.2 | 移除 TCN Encoder 导致面部重建和身体多样性下降 |
| 核归一化 | 卷积输出除以核大小 | Eq.5 | 提升训练稳定性 |
| 注意力残差解码 | TransTCN + 注意力残差融合 | Eq.4 | 移除后 FGD 升至 6.178 |
| 粗到细预测 | 从粗尺度逐层迭代预测 | Eq.13 | 金字塔层数实验：4 层最优 |

**证据强度说明：** 上述公式均来自论文 Sec 3.3 和 Sec 3.4 的明确描述，消融实验（Table 2、Table 5）提供了因果证据。注意力图可视化（Figure 3）进一步验证了不同身体部位对多尺度 token 的差异化关注——面部偏好细粒度 token，下半身偏好粗粒度 token，为金字塔表征的合理性提供了解释性支撑。

### 补充图表

![[assets/figures/papers/neurips_2025_pyramotion/figures/001_Figure_1.jpg]]
*Figure 1: Illustration of gesture sequences with expressive motion patterns in different durations*

![[assets/figures/papers/neurips_2025_pyramotion/figures/006_Figure_3.jpg]]
*Figure 3: Attention Map Visualization*



## 实验与关键发现

### 整体性能对比

PyraMotion 在 BEAT2 数据集上与当前最强方法进行了全面对比（Table 1）。结果表明，PyraMotion 在所有关键指标上均取得最优或次优表现：

![[assets/figures/papers/neurips_2025_pyramotion/figures/003_Table_1.jpg]]
*Table 1: In this part, we compare the overall performances of M3G with classical and state-of-the-art audiodriven gesture generation methods. In Table 1, Habibie et al‡ and TalkSHOW‡ denotes the reported performance of reproduced full-body motion generation in [22], ∗ denotes the results are directly adapted from their original paper due to the same experimental settings, thus no std values are reported. AMUSE† denotes the reported performance is by the reproduced evaluation code by ourselves*

![[assets/figures/papers/neurips_2025_pyramotion/figures/005_Table_3.jpg]]
*Table 3: presents the joints’ rotation Mean Square Error (JRMSE) for each body part compared to the ground truth sequences. The second part of the table shows the metrics used in Table 1 to assess the reconstruction performance based on the encoded tokens in APVQ-VAE*

- **FGD（Fréchet Gesture Distance）**：4.612，显著低于其他方法，表明生成手势的分布与真实手势最为接近。
- **MSE**：7.176 ± 0.028，在重建精度上达到最优。
- **LVD（L1 Velocity Difference）**：7.270 ± 0.011，运动速度曲线与真值的一致性最高。

对比的基线方法包括 **CaMN**（Liu et al., CVPR 2024）、**EMAGE**（Yi et al., CVPR 2023）、**DiffuseStyleGesture**（Yang et al., arXiv 2023）、**Gesture2Vec**（Yazdian et al., IROS 2022）、**TalkSHOW**（Yoon et al., TOG 2020）以及 Habibie et al. 的全身边手势生成方法。PyraMotion 在这些强基线面前展现了全面的性能优势，验证了多尺度金字塔运动表示与注意力融合机制的有效性。所有实验指标均重复运行 5 次并报告标准差，确保结果的统计可靠性。

### 消融实验分析

为验证各核心组件的贡献，论文进行了系统性的消融实验（Table 2），主要结论如下：

![[assets/figures/papers/neurips_2025_pyramotion/figures/004_Table_2.jpg]]
*Table 2: reported that the PyraMotion significantly outperforms or performs similarly with all variants, demonstrating the contributions of these components. Moreover, the results indicate that replacing the TransTCN structure leads to a more significant decline in performance compared with the other two variants, demonstrating the indispensability of the token decoding process in the overall workflow. The absence of Full-Body latent mainly affects the body’s reconstructing performance, which might be caused by the lack of mutual information among different body parts. The w/o TCN Encoder performs significantly worse than PyraMotion on facial reconstruction and body diversity, indicating the ability...*

**TransTCN 解码器的关键作用**：移除 TransTCN 结构（即用 Eq.2 的普通 TCN 替代 Eq.4 的注意力残差解码器）导致性能全面崩溃——FGD 从 4.612 升至 6.178，BC 升至 7.132，Diversity 升至 12.869，MSE 升至 8.833，LVD 升至 9.511。这一剧烈退化表明，注意力残差融合设计是高质量手势重建与生成的核心瓶颈组件。TransTCN 通过堆叠多尺度重建结果并利用注意力机制计算残差，有效整合了不同时间粒度的运动信息。

**金字塔 TCN 编码器的必要性**：去除 TCN Encoder 变体在面部重建和身体运动多样性上出现明显下降。金字塔 TCN 编码器能够捕捉不同时间尺度的运动模式，对面部表情这类细粒度信号和身体运动的多样性建模均不可或缺。

**全身隐含表示的互信息贡献**：去除 Full-Body Latent 后，身体部位间的互信息被削弱，导致身体重建性能衰减。这验证了在部位独立建模的基础上保留全局隐含表示对于协调多部位运动一致性的重要性。

### 重建质量对比

APVQ-VAE 与普通 VQ-VAE 的重建误差对比（Table 3）进一步揭示了多尺度编码的优势。APVQ-VAE 在各身体部位均取得更低的关节旋转均方根误差（JRMSE）：

- 面部：1.044
- 上半身：2.955
- 手部：4.662
- 下半身：2.209
- 全局位移：5.129

在整体重建指标上，APVQ-VAE 的 FGD 仅为 1.296（远优于普通 VQ-VAE），BC 为 7.237，Diversity 为 12.864，MSE 为 0.279。这一结果直接证明了多尺度金字塔编码与共享码本量化策略在运动重建精度上的显著增益。

### 金字塔层数选择

金字塔层数的消融实验（Table 5）表明，4 层结构在重建与生成指标间取得最佳平衡。5 层金字塔引入了过拟合，导致性能下降。当前方法需要手动设定层数，无法根据数据集特性自适应调整，这是 PyraMotion 的一个已知局限。

![[assets/figures/papers/neurips_2025_pyramotion/figures/008_Table_5.jpg]]
*Table 5: Experiments for Pyramid Layer Number Selection*

### 推理效率

推理时间对比（Table 4）显示，PyraMotion 的推理耗时约 41 秒，长于 EMAGE 的约 22 秒。虽然 PyraMotion 在生成质量上显著领先，但实时部署仍面临效率挑战，这是未来优化的方向之一。

![[assets/figures/papers/neurips_2025_pyramotion/figures/007_Table_4.jpg]]
*Table 4: Inference Time Comparison*

### 可视化分析

注意力图可视化（Figure 3）揭示了不同身体部位对多尺度 token 的差异化偏好：面部倾向于关注细粒度时间尺度的 token，而下半身则偏好粗粒度 token。这一发现从可解释性角度验证了金字塔多尺度表示设计的合理性——不同身体部位的运动确实具有不同的特征时间尺度，统一建模会抹平这种差异。

### 用户感知研究

用户感知研究（Figure 4）通过人类主观评价进一步验证了 PyraMotion 生成手势的自然度和表现力优势。研究经过 IRB 批准，确保了伦理合规性。

![[assets/figures/papers/neurips_2025_pyramotion/figures/009_Figure_4.jpg]]
*Figure 4: Perceptual Study*



## 定位与知识库关联

### 与现有工作的关系

PyraMotion 的核心贡献在于对 VQ-VAE 运动表征的时间尺度瓶颈进行了根本性改造。此前的主流方法——无论是基于 VQ-VAE 的 **EMAGE** (Yi et al., CVPR 2023)、**CaMN** (Liu et al., CVPR 2024)，还是基于扩散/回归的 **DiffuseStyleGesture** (Yang et al., arXiv 2023)、**TalkSHOW** (Yoon et al., TOG 2020)——均以固定帧数对全身运动进行统一编码或生成。这种单尺度范式隐含假设所有身体部位的运动模式具有相同的时间粒度，显然与事实相悖：面部表情变化极快（百毫秒级），而身体姿态调整和位移则跨越数秒。

PyraMotion 的突破点在于将计算机视觉中成熟的特征金字塔思想迁移至运动生成领域，构建了**多尺度金字塔运动表示**。具体而言，APVQ-VAE 使用 $n$ 个不同时间尺度的 TCN 分别编码原始手势序列，产生从细粒度到粗粒度的嵌入序列 $\mathbf{F} = [\mathbf{f}_1, ..., \mathbf{f}_n]$，所有尺度共享同一码本 $\mathbf{Z}$ 以保证语义一致性。这种设计使模型能够同时捕捉短时快速动作与长时缓慢姿态变化，为后续的注意力融合提供了多粒度信息基础。

与 **Gesture2Vec** (Yazdian et al., IROS 2022) 等将手势聚类为离散类别的思路不同，PyraMotion 的离散化发生在隐空间而非语义空间，保留了连续运动的丰富性。同时，其分部位建模策略（面部、上半身、手部、下半身独立提取特征再融合）与 Habibie et al. 的全身体系统一建模形成对比，使得不同部位可以自主关注适合自身的时间尺度——Figure 3 的注意力图直观证实了这一假设：面部偏好细粒度 token，而下半身偏好粗粒度 token。

### 适用边界

PyraMotion 的设计假设和实验设定决定了其适用边界：

1. **模态限制**：当前框架仅支持语音+文本的双模态输入，通过注意力机制融合节奏音频特征 $\mathbf{r}_{1:T}$ 与文本内容特征 $\mathbf{c}_{1:T}$。不支持额外条件控制（如情感标签、说话风格、环境音），无法直接迁移至音乐驱动或纯文本驱动的动作生成场景。

2. **金字塔层数的刚性**：层数 $n$ 为固定超参数（实验确定 4 层最优），模型不具备根据输入数据动态调整层数的能力。Table 5 显示 5 层引入过拟合导致性能下降，表明更深金字塔的收益递减，但这可能受限于 BEAT2 数据集的运动模式多样性。

3. **推理效率**：Table 4 显示 PyraMotion 推理时间约 41 秒，显著长于 EMAGE 的约 22 秒。粗到细的多尺度迭代预测和 TCAT 模块引入了额外计算开销，限制了实时应用场景的部署可行性。

4. **数据依赖**：所有实验均在 BEAT2 数据集上进行，该数据集以英语演讲场景为主，手势风格相对规范。模型在非英语语音、自由对话、多人交互等场景下的泛化能力未经验证。

### 局限与开放问题

**已验证的局限**：

- **金字塔层数需手动选择**：模型无法根据数据集特性自适应调整层数。Table 5 的消融实验虽然给出了 4 层最优的经验结论，但这一结论的数据集依赖性尚不明确。
- **不支持多模态条件控制**：当前框架仅接受语音和文本输入，无法通过文本风格描述、情感标签等额外条件引导生成。
- **推理时间较长**：约 41 秒的推理时长使其难以满足实时交互需求，尽管论文指出这主要受限于 token 预测器的自回归特性。
- **代码尚未开源**：尽管论文声称代码和数据将在接收后开源，但截至分析时点，可复现性依赖后续发布。

**开放问题**：

1. **自适应金字塔层数**：能否设计门控机制或基于运动复杂度的动态层数选择策略，使模型在简单运动场景下使用较少层数以加速推理，在复杂场景下自动增加层数？

2. **部位间关联与独立的平衡**：当前分部位独立建模后通过 TCAT 融合，消融实验显示移除 Full-Body Latent 会削弱部位间互信息。如何在保持部位独立性的同时更精细地建模跨部位协调关系（如手部与面部在强调语气时的协同）？

3. **多尺度表征的跨模态泛化**：金字塔运动表征的核心思想——不同时间尺度捕捉不同粒度的动态模式——是否可推广至音乐驱动舞蹈生成、环境声驱动反应动作等其他时间序列到运动的映射任务？

4. **金字塔表征的可解释性深化**：Figure 3 的注意力图揭示了不同部位的时间尺度偏好，但各层的 token 究竟编码了何种运动语义（如节奏模式、姿态过渡、情感表达）仍不清晰。进一步的可解释性分析可能为模型改进提供方向。



## 原文 PDF

![[paperPDFs/NEURIPS_2025/PyraMotion_Attentional_Pyramid-Structured_Motion_Integration_for_Co-Speech_3D_Gesture_Synthesis.pdf]]

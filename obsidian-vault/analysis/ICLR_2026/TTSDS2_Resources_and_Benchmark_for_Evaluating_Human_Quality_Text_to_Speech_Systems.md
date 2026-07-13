---
title: "TTSDS2: Resources and Benchmark for Evaluating Human-Quality Text to Speech Systems"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/TTSDS2_Resources_and_Benchmark_for_Evaluating_Human_Quality_Text_to_Speech_Systems.pdf
project_link: null
code_link: null
openreview_forum_id: uGai5lYHlV
aliases:
- TTSDS2
tags:
- ICLR_2026
- topic/optimization_theory_probabilistic
- topic/optimization_theory_probabilistic/optimization_methods
core_operator: "将评估框架定义为分布相似性问题：通过Wasserstein距离比较合成语音与真实参考和噪声参考在多个感知因子上的分布，并将其归一化为0-100的评分。"
primary_logic: "集成多个感知因子并采用无监督的简单平均聚合，使TTSDS2成为在未见域和语言上保持稳健相关性的客观指标，超越了单一指标的黑箱行为。"
claims:
- "在四个数据集的三项主观评分上，TTSDS2是唯一在所有情况下Spearman相关系数均超过0.5的指标，平均0.67。"
- "TTSDS2在Clean域的MOS相关性为0.75，显著优于前身TTSDS的0.60。"
- "TTSDS2的简单平均因子权重在留一法交叉验证中优于学习到的权重，证明其无需领域微调即可泛化。"
- "CLEAN (LibriTTS) 上 MOS Spearman ρ = 0.75"
---

# TTSDS2: Resources and Benchmark for Evaluating Human-Quality Text to Speech Systems

> [!tip] 核心洞察
> 集成多个感知因子并采用无监督的简单平均聚合，使TTSDS2成为在未见域和语言上保持稳健相关性的客观指标，超越了单一指标的黑箱行为。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | TTSDS2：评估人类级文本到语音系统的资源和基准 |
| 英文题名 | TTSDS2: Resources and Benchmark for Evaluating Human-Quality Text to Speech Systems |
| 会议/期刊 | ICLR 2026 (Oral) |
| Links | [paper](https://openreview.net/forum?id=uGai5lYHlV) |
| Topic | #topic/optimization_theory_probabilistic #topic/optimization_theory_probabilistic/optimization_methods |
| Method | TTSDS2 |
| Dataset | CLEAN (LibriTTS), WILD (YouTube), KIDS (儿童语音), 全部四个域平均 |

> [!tip] 效果简介
> - CLEAN (LibriTTS) 上，MOS Spearman ρ 为 0.75，对比 0.60 (TTSDS)，变化 +0.15。
> - WILD (YouTube) 上，MOS Spearman ρ 为 0.75，对比 0.67 (TTSDS)，变化 +0.08。
> - KIDS (儿童语音) 上，MOS Spearman ρ 为 0.61，对比 0.70 (TTSDS, 略优)，变化 -0.09。

## 概要

当合成语音质量逼近人类水平时，如何可靠、可比较地评估不同系统成为一个核心瓶颈。传统主观听测资源密集、不可跨研究比较，而现有客观指标在跨域和跨语言场景下与人类判断的相关性高度不一致，难以胜任高质量系统的可靠区分。

本文提出 **TTSDS2**，将评估问题形式化为**分布相似性度量**：通过计算合成语音与真实参考、噪声参考在多个感知因子（GENERIC、SPEAKER、PROSODY、INTELLIGIBILITY）上的 Wasserstein 距离，并将其归一化为 0–100 的评分。该方法的核心洞察在于：集成多感知因子并采用无监督的简单平均聚合，使 TTSDS2 在未见域和语言上保持了稳健的相关性，超越了单一指标的黑箱行为。

在四个数据集、三项主观评分上的系统性验证表明，TTSDS2 是 16 个对比指标中**唯一在所有条件下 Spearman 相关系数均超过 0.5** 的指标，平均相关系数达到 0.67。其中，在 Clean 域的 MOS 相关性为 0.75，显著优于其前身 TTSDS 的 0.60。留一法交叉验证进一步证实，简单平均因子权重在三个域上优于学习到的权重，证明该方法无需领域微调即可泛化。

论文同时发布了可复现的评估流水线，覆盖 14 种语言和 20 个 2022 年后发布的 TTS 系统，为社区提供了一套可自动更新、无污染的基准测试框架。

### 文本到语音评估的瓶颈

随着深度学习驱动的文本到语音（TTS）系统在自然度和表现力上逼近人类水平，如何可靠地评估这些系统成为一个日益紧迫的问题。主观听测（如MOS、CMOS）虽然仍是评估语音质量的“金标准”，但其资源密集、周期漫长，且不同研究团队之间的评测结果难以直接比较。另一方面，现有的客观指标面临两个核心挑战：**跨域泛化能力不足**和**与人类感知的相关性不一致**。

具体而言，当合成语音从明显的机械感进化到接近真人的细腻表达时，传统信号级指标（如MCD、PESQ、STOI）的区分力急剧下降。即便是近年来涌现的基于神经网络的MOS预测器，如**UTMOS** (Saeki et al., 2022)、**NISQA** (Mittag et al., 2021) 和**SQUIM MOS** (Kumar et al., 2023)，虽然在特定训练域内表现良好，但在面对未见过的声学环境、说话风格或语言时，其预测相关性往往大幅波动。这一缺口意味着：**当合成语音达到人类水平时，主观评估资源密集且不可比较，现有客观指标在跨域和语言上的相关性不一致，难以可靠地区分高质量系统。**

### TTSDS的初步尝试与遗留问题

为应对上述挑战，**TTSDS**（Minixhofer et al., 2024）提出了一种范式转换：将评估重新定义为**分布相似性问题**。其核心思想是，不再逐样本预测MOS分数，而是通过比较合成语音与真实语音在多个感知因子上的特征分布差异来量化质量。具体而言，TTSDS利用Wasserstein距离衡量合成语音分布与真实参考分布、噪声参考分布之间的差异，并将其归一化为0–100的评分。

然而，TTSDS在以下方面存在明显局限：

1. **特征设计的鲁棒性不足**：可懂度因子依赖词错误率（WER），这在跨语言场景下高度依赖ASR模型的性能；韵律因子使用HuBERT token长度，实验发现该特征会导致系统性低分。
2. **跨域泛化未经验证**：TTSDS仅在受控的干净语音域上进行了初步验证，其在噪声环境、自然采集语音、儿童语音等多样化条件下的表现尚不明确。
3. **语言覆盖有限**：原始TTSDS以英语为中心，未系统评估多语言场景下的有效性。

### TTSDS2的动机与目标

本文提出**TTSDS2**，旨在解决TTSDS的上述遗留问题，并构建一个可复现、可扩展的多语言TTS评估基准。其核心动机可概括为三个层面：

- **提升指标的鲁棒性**：通过重新设计感知因子（用ASR模型激活替代WER、用说话速率替代token长度、引入WavLM增强多样性），使指标在未见域和语言上保持稳定的相关性。
- **建立可信的泛化证据**：在四个差异显著的域（Clean、Noisy、Wild、Kids）和三种主观评分（MOS、CMOS、SMOS）上，与16个公开指标进行系统性对比，提供严格的统计证据。
- **构建可持续的评估基础设施**：发布自动化流水线，定期从YouTube抓取多语言数据、合成样本并计算TTSDS2分数，使基准能够随时间演化，避免数据污染和系统过时。

最终，TTSDS2的目标不是取代主观听测，而是提供一个**与人类判断高度一致、跨域跨语言稳健、且无需额外训练即可直接部署**的客观评估工具，为TTS研究的快速迭代提供可靠的质量信号。

## 核心方法与创新机理

TTSDS2 的核心创新并非提出全新的评估范式，而是对 **TTSDS**（Minixhofer et al., 2024）分布相似性框架的深度重构，使其在跨域和跨语言场景下获得稳健的泛化能力。其关键洞察在于：当合成语音逼近人类水平时，单一指标的“黑箱”行为导致相关性高度不稳定；唯有将评估分解为多个感知因子，并通过无监督的简单聚合，才能在未见域上保持一致性。

### 从 WER 到 ASR 潜在表征：可懂度因子的重构

TTSDS 原始框架中，**INTELLIGIBILITY** 因子直接依赖词错误率（WER）。然而 WER 在高质量合成语音上趋于饱和，丧失了区分度。TTSDS2 将其替换为语音识别模型（whisper、wav2vec 2.0）的最终层激活分布（Section 2）。这一改动将可懂度评估从离散的转录正确性提升为连续的**感知空间对齐**：即使转录完全正确，合成语音与真实语音在 ASR 模型内部表征上的分布差异仍能反映微妙的可懂度退化。该改动是 TTSDS2 在 Clean 域 MOS 相关性从 0.60 跃升至 0.75 的关键驱动力之一（Table 3）。

### 从 token 长度到说话速率：韵律因子的修正

TTSDS 的 **PROSODY** 因子使用 HuBERT token 长度作为韵律特征，但作者发现该特征“导致低分”（Section 2）。TTSDS2 转而计算 HuBERT 和 Allosaurus 的去重 token 说话速率（utterance-level speaking rate）。这一修正解决了原始特征对韵律质量的不当惩罚，使韵律因子与人类感知的对齐更加准确。

### 增加 WavLM 以提升通用因子多样性

**GENERIC** 因子在 TTSDS 中仅使用 HuBERT 和 wav2vec 2.0 特征。TTSDS2 增加了 WavLM 特征以“增加多样性”（Section 2）。这一扩展并非简单堆砌，而是通过引入不同预训练目标的表征，使通用因子捕获更丰富的声学属性分布，从而在噪声域和野外域中保持稳健。

### 简单平均作为正则化：拒绝学习到的权重

TTSDS2 最关键的架构决策是采用**未加权的简单平均**聚合因子得分，而非通过学习到的权重最大化训练域相关性。留一法交叉验证（Table 4）显示，简单平均在四个域中的三个域上优于学习到的权重。学习到的权重表现出极高的不稳定性：在 Table 5 中，GENERIC 因子的系数在不同训练域间从 -0.162 波动至 0.066，甚至出现负值。这表明在有限域上优化权重会导致严重的过拟合，而简单平均天然充当了**域无关的正则化手段**，使 TTSDS2 无需任何领域微调即可泛化。

### 归一化框架的继承与固化

TTSDS2 沿用了基于 Wasserstein 距离的归一化评分公式（Equation 1）：

$$\mathrm{TTSDS2}(D, \tilde{D}, \mathfrak{D}^{\mathrm{NOISE}}) = 100 \times \frac{W_{2}^{\mathrm{NOISE}}}{W_{2}^{\mathrm{REAL}} + W_{2}^{\mathrm{NOISE}}}$$

该公式将合成语音的分布相似性量化为 0–100 的评分：0 表示等同于噪声参考，100 表示等同于真实参考，50 以上表示更接近真实语音。这一归一化框架本身并非创新，但 TTSDS2 通过前述因子层面的重构，使其在四个域和 14 种语言上首次实现了所有主观评分均超过 0.5 的 Spearman 相关性（Table 3），成为 16 个对比指标中唯一达成此目标的指标。

### 创新边界与待验证点

TTSDS2 的创新集中在**因子特征替换**和**聚合策略简化**两个层面，未改变分布相似性的底层数学框架。其跨语言泛化能力（Figure 3）目前仅覆盖 14 种语言，且多语言模型仍以英语为中心，非英语语言的评估全面性有待进一步验证。

TTSDS2 将合成语音质量的评估定义为一个**分布相似性问题**：给定合成语音集合 $\tilde{D}$、真实参考语音集合 $D$ 和噪声参考集合 $\mathfrak{D}^{\mathrm{NOISE}}$，通过比较合成语音与两类参考在多个感知因子上的特征分布距离，得出一个归一化的质量评分。其核心假设是：高质量的合成语音应与真实语音在感知特征上具有高度相似的分布，而与噪声分布保持明显距离。

### 评估因子分解

TTSDS2 采用因子化的评估框架，将语音质量分解为四个感知驱动的维度：

- **GENERIC（通用质量）**：使用 HuBERT、wav2vec 2.0 和 WavLM 等多层自监督模型的最终层激活，捕捉语音的整体自然度。相比前身 TTSDS，新增 WavLM 以增加特征多样性。
- **SPEAKER（说话人身份）**：通过说话人嵌入（如 X-Vector 和 ECAPA-TDNN）衡量合成语音是否保持了目标说话人的身份特征。
- **PROSODY（韵律）**：使用 HuBERT 和 Allosaurus 的去重 token 序列计算话语级说活速率，替代了原 TTSDS 中表现不佳的 token 长度特征。
- **INTELLIGIBILITY（可懂度）**：不再依赖词错误率（WER），转而使用 ASR 模型（whisper、wav2vec 2.0）的最终层激活来评估语音的可理解性。

每个因子内部包含若干特征表示（详见 Table 1），各特征得分取平均得到因子得分，四个因子得分再取**无加权算术平均**得到最终的 TTSDS2 总分。这一简单平均策略被消融实验证实具有优于学习权重的泛化能力（见 Table 4 和 Table 5）。

### 分布距离计算与归一化

对于每个特征，TTSDS2 计算合成语音分布与真实参考分布之间的 Wasserstein 距离。在多变量高斯近似下，平方 2-Wasserstein 距离具有闭式解：

$$W_{2}(D, \tilde{D})^{2} = \left\| \mu - \tilde{\mu} \right\|_{2}^{2} + \mathrm{Tr}\left( \Sigma + \tilde{\Sigma} - 2(\tilde{\Sigma}^{1/2} \Sigma \tilde{\Sigma}^{1/2})^{1/2} \right)$$

对于一维特征（如基频 $F_0$），则使用基于逆累积分布函数的简化形式：

$$W_{2}(D, \tilde{D})^{2} = \int_{0}^{1} (C^{-1}(z) - \tilde{C}^{-1}(z))^{2} dz$$

最终的 TTSDS2 归一化得分将合成语音到真实语音的距离 $W_{2}^{\mathrm{REAL}}$ 和到噪声的距离 $W_{2}^{\mathrm{NOISE}}$ 映射到 0–100 区间：

$$\mathrm{TTSDS2}(D, \tilde{D}, \mathfrak{D}^{\mathrm{NOISE}}) = 100 \times \frac{W_{2}^{\mathrm{NOISE}}}{W_{2}^{\mathrm{REAL}} + W_{2}^{\mathrm{NOISE}}}$$

其中，0 表示与噪声分布完全一致，100 表示与真实语音分布完全一致，大于 50 表示更接近真实语音而非噪声。这一归一化机制使得 TTSDS2 在不同域和语言间具有可比性，无需针对特定测试集进行校准。

### 自动化基准流水线

为支持持续更新的多语言评估，TTSDS2 配套提供了一个自动化流水线（Algorithm 1），包含五个模块化步骤：

1. **Data Scraping**：定期从 YouTube 抓取多语言音频数据。
2. **Preprocessing**：依次执行语音活动检测、说话人分离、ASR 转录和语音增强。
3. **Filtering**：使用 XNLI 过滤争议内容，Pyannote 检查串扰，Demucs 检测背景音乐，确保参考数据质量。
4. **Synthesis**：为所有待评估的 TTS 系统生成合成语音样本。
5. **TTSDS2 Scoring**：计算各因子得分和总体 TTSDS2 分数，生成自动化排名。

该流水线覆盖 14 种语言，所有特征选择在相关性实验之前即已最终确定，并通过将真实数据随机分成两半计算 TTSDS 得分来验证特征的稳健性——真实语音的一半应对另一半获得接近 100 的得分。

### 输入输出流

- **输入**：合成语音集合 $\tilde{D}$、真实参考语音集合 $D$、噪声参考集合 $\mathfrak{D}^{\mathrm{NOISE}}$。
- **中间表示**：各特征提取器输出的嵌入或标量序列，经分布建模后计算 Wasserstein 距离。
- **输出**：四个因子得分及一个 0–100 的总体 TTSDS2 得分，得分越高表示合成语音越接近真实语音质量。

需要指出的是，TTSDS2 的 Wasserstein 距离计算为 CPU 密集型，每次评估约需 9.4 分钟，且当前仅适用于 3–30 秒的短句，无法评估长篇语音的连贯性或风格适应性。

### 评估框架：分布相似性建模

TTSDS2 将合成语音的质量评估定义为一个**分布相似性问题**。其核心假设是：高质量的合成语音应在多个感知因子上，与真实语音的分布足够接近，而与噪声语音的分布足够远。

评估框架包含四个感知因子，每个因子通过一组特征表示来度量：

- **GENERIC（通用质量）**：使用 HuBERT、wav2vec 2.0 和 WavLM 的表示，捕获语音的整体自然度。相比前身 TTSDS，新增 WavLM 以增加特征多样性。
- **SPEAKER（说话人相似度）**：使用说话人验证模型的嵌入（如 ECAPA-TDNN），度量合成语音与目标说话人的身份一致性。
- **PROSODY（韵律）**：使用 HuBERT 和 Allosaurus 的去重 token 说话速率，替代了 TTSDS 中基于 token 长度的特征。原 token 长度特征在高质量系统上得分过低，说话速率特征更准确地反映韵律自然度。
- **INTELLIGIBILITY（可懂度）**：使用 ASR 模型（whisper、wav2vec 2.0）的最终层激活，替代了 TTSDS 中的词错误率（WER）。这一改变避免了 WER 在高质量语音上饱和而无法区分的问题。

### 核心公式：Wasserstein 距离与归一化得分

TTSDS2 使用 **2-Wasserstein 距离**（Earth Mover's Distance）度量合成语音特征分布与参考分布之间的差异。对于多变量高斯近似，其平方形式为：

$$W_{2}(D, \tilde{D})^{2} = \left\| \mu - \tilde{\mu} \right\|_{2}^{2} + \mathrm{Tr}\left( \Sigma + \tilde{\Sigma} - 2(\tilde{\Sigma}^{1/2} \Sigma \tilde{\Sigma}^{1/2})^{1/2} \right)$$

其中 $D$ 和 $\tilde{D}$ 分别为真实和合成语音的特征分布，$\mu$、$\tilde{\mu}$ 为均值向量，$\Sigma$、$\tilde{\Sigma}$ 为协方差矩阵。第一项度量均值偏移，第二项（迹项）度量协方差结构的差异。

对于一维特征（如基频 $F_0$），存在基于逆累积分布函数的封闭解：

$$W_{2}(D, \tilde{D})^{2} = \int_{0}^{1} (C^{-1}(z) - \tilde{C}^{-1}(z))^{2} dz$$

其中 $C^{-1}$ 和 $\tilde{C}^{-1}$ 分别为两个分布的逆累积分布函数。

**归一化得分**：将合成语音 $D$ 与真实参考 $\tilde{D}$ 和噪声参考 $\mathfrak{D}^{\mathrm{NOISE}}$ 的 Wasserstein 距离进行归一化，得到 0–100 的评分：

$$\mathrm{TTSDS2}(D, \tilde{D}, \mathfrak{D}^{\mathrm{NOISE}}) = 100 \times \frac{W_{2}^{\mathrm{NOISE}}}{W_{2}^{\mathrm{REAL}} + W_{2}^{\mathrm{NOISE}}}$$

其中 $W_{2}^{\mathrm{REAL}} = W_{2}(D, \tilde{D})$ 是合成语音到真实语音的距离，$W_{2}^{\mathrm{NOISE}} = W_{2}(D, \mathfrak{D}^{\mathrm{NOISE}})$ 是合成语音到噪声参考的距离。得分 $>50$ 表示更接近真实语音，得分 $<50$ 表示更接近噪声。

### 因子聚合策略

每个因子的得分由其所含特征的 Wasserstein 归一化得分取平均得到，最终 TTSDS2 得分为四个因子得分的**简单算术平均**。消融实验（Table 4）表明，这种无监督的等权重聚合在留一法跨域验证中优于通过线性回归学习到的权重——学习权重在训练域上表现出高方差，甚至出现负系数（Table 5），证实简单平均作为一种隐式正则化手段对泛化至关重要。

### 自动化基准流水线

TTSDS2 提供了一个可重复运行的自动化基准流水线（Algorithm 1），包含五个模块：

1. **Data Scraping**：定期从 YouTube 抓取多语言音频。
2. **Preprocessing**：语音活动检测、说话人分离、ASR 转录、语音增强。
3. **Filtering**：使用 XNLI 过滤争议内容，Pyannote 检查串扰，Demucs 检测背景音乐。
4. **Synthesis**：为所有评估的 TTS 系统生成合成语音样本。
5. **TTSDS2 Scoring**：计算各因子得分和总体 TTSDS2 得分。

该流水线使得基准数据集可以定期重建，避免数据污染，并支持 14 种语言的自动化系统排名。

## 实验与关键发现

### 评估框架与数据集构建

TTSDS2的验证建立在四个差异化域的数据集之上：**CLEAN**（LibriTTS，标准朗读语音）、**NOISY**（未经SNR过滤的LibriVox录音）、**WILD**（YouTube多语言抓取数据）和**KIDS**（儿童语音）。这种设计刻意覆盖了从受控朗读到真实世界噪声、从成人到儿童声学特征的广泛变异，以检验指标的跨域稳健性。

主观评分通过Prolific平台招募200名英美本土英语讲者采集，每位听者仅参与一个域的评估以避免顺序效应。采集维度包括MOS（整体自然度）、CMOS（与真实参考的比较偏好）和SMOS（说话人相似度），并经过注意力检查筛选以保证标注质量。该研究已通过伦理审查（编号112246），参与者在知情同意后参与，30天内有权撤回同意。

### 主结果：跨域相关性的全面优势

Table 3呈现了TTSDS2与16个基线指标在四个域、三项主观评分上的Spearman秩相关系数。**TTSDS2是唯一在所有12种条件下ρ均超过0.5的指标**，平均相关系数达到0.67，较其前身TTSDS（平均0.61）相对提升约10%。

![[assets/figures/papers/paper_list_l38_https_openreview_net_forum_id_uGai5lYHlV/figures/004_Table_3.jpg]]
*Table 3: Spearman rank correlations. Colours: –1 . . . –0.5, –0.5 . . . 0, 0 . . . 0.5, 0.5 . . . 1*

关键对比数据如下：

| 域 | 指标 | TTSDS2 ρ | TTSDS ρ | 最佳基线 |
|---|------|----------|---------|---------|
| CLEAN | MOS | **0.75** | 0.60 | RawNet3 0.73 |
| WILD | MOS | **0.75** | 0.67 | X-Vector 0.68 |
| KIDS | MOS | 0.61 | **0.70** | TTSDS 0.70 |
| 四域平均 | 综合 | **0.67** | 0.61 | — |

在CLEAN域上，TTSDS2的MOS相关性从TTSDS的0.60显著跃升至0.75，这是特征集改进的直接效果。在WILD域上，TTSDS2同样达到0.75，证明其在真实世界噪声条件下的稳健性。KIDS域是TTSDS2唯一略逊于前身的场景（0.61 vs 0.70），这可能与儿童语音的声学特性（更高的基频、更快的语速）对现有特征提取器的挑战有关，提示该域仍需针对性优化。

Figure 2通过散点图直观展示了三个代表性指标（TTSDS2、X-Vector说话人相似度、SQUIM MOS）与人类MOS的关系。TTSDS2在不同域的数据点沿整体拟合线紧密分布，而X-Vector和SQUIM MOS则呈现明显的域间聚类偏移——这是分布相似性方法相对于点估计方法的固有优势。

### 消融实验：简单平均的泛化优势

TTSDS2的最终得分由四个因子（GENERIC、SPEAKER、PROSODY、INTELLIGIBILITY）的未加权算术平均得出。Table 4的留一法交叉验证（LOOCV）实验检验了这一设计选择：在三个域上训练线性回归权重以最大化与MOS的相关性，在第四个留出域上测试。

![[assets/figures/papers/paper_list_l38_https_openreview_net_forum_id_uGai5lYHlV/figures/006_Table_4.jpg]]
*Table 4: Leave-One-Out Cross-Validation (Generalisation). Evaluation on a held-out domain after training on the other three*

结果清晰表明：**简单平均在四个留出域中的三个域上优于学习到的权重**。具体而言，简单平均在CLEAN（0.747 vs 0.645）、NOISY（0.590 vs 0.514）和WILD（0.752 vs 0.658）上均表现更佳，仅在KIDS域上学习权重以0.853显著领先。这表明KIDS域中某些因子的重要性与其他域存在系统性差异，但同时也说明简单平均作为一种强正则化手段，在大多数未见域上提供了更可靠的泛化保证。

Table 5进一步揭示了学习权重的内在不稳定性。以GENERIC因子为例，其最优系数在不同训练域间从-0.162波动至+0.066，甚至出现负值——这意味着在某些训练域上学到的权重会惩罚在MOS上实际有正向贡献的因子。这种高方差和符号反转现象证实了简单平均作为先验的必要性：在缺乏目标域标注的情况下，假设各因子等权贡献是最安全的选择。

![[assets/figures/papers/paper_list_l38_https_openreview_net_forum_id_uGai5lYHlV/figures/007_Table_5.jpg]]
*Table 5: Instability of learned weights. Optimal coefficients vary drastically by training domain, occasionally becoming negative*

### 失败模式与局限性

尽管TTSDS2在跨域相关性上表现突出，但**即使是表现最好的指标，Spearman相关系数也从未超过0.8**。这一上限表明主观听测中存在无法被任何客观指标完全解释的噪声或感知成分，可能源于个体听者的审美偏好、注意力波动或对特定声学伪影的敏感度差异。

计算开销是另一个实际瓶颈。TTSDS2的Wasserstein距离计算为CPU密集型，单次评估约需**9.4分钟**，这限制了其在大规模实时基准测试中的应用。论文已提出使用最大均值差异（MMD）等替代距离度量作为未来的加速方向，但尚未验证其相关性保持情况。

此外，当前评估仅限于3-30秒的短句，无法评估长篇语音的连贯性、风格适应性或跨句韵律一致性。随着TTS系统越来越多地应用于有声书生成、对话系统等长文本场景，这一局限将日益突出。

### 多语言基准的构建与验证

TTSDS2不仅是一个指标，还配套提供了一个自动化基准构建管道（Algorithm 1），包括数据抓取、预处理（语音活动检测、说话人分离、ASR转录、语音增强）、过滤（XNLI争议内容检测、Pyannote串扰检查、Demucs背景音乐检测）、合成和TTSDS2评分五个步骤。该管道可定期重建多语言数据集，避免训练数据污染。

多语言验证显示，TTSDS2得分与语言类型学距离呈显著负相关（ρ=-0.51），表明指标能够捕捉到因语言差异导致的合成质量变化。Figure 3展示了14种语言的TTSDS2得分分布，但当前多语言模型仍以英语为中心，非英语语言的评估覆盖面和深度有待扩展。

![[assets/figures/papers/paper_list_l38_https_openreview_net_forum_id_uGai5lYHlV/figures/001_Table_1.jpg]]
*Table 1: Feature set used for TTSDS compared to TTSDS2*

![[assets/figures/papers/paper_list_l38_https_openreview_net_forum_id_uGai5lYHlV/figures/003_Table_2.jpg]]
*Table 2: Mean over datasets of MOS, CMOS, SMOS and the corresponding TTSDS2 score*

![[assets/figures/papers/paper_list_l38_https_openreview_net_forum_id_uGai5lYHlV/figures/009_Table_6.jpg]]
*Table 6: Open-source TTS systems, prior evaluation, and results for each system relative to ground-truth (GT) speech: † = accompanied by publication; ∗ = third-party implementation; Parity column: Reported MOS/CMOS are close to GT (∼), surpassing GT (>) or below GT (\<)*

## 定位与知识库关联

### 问题定位：高质量合成语音的评估困境

TTSDS2 试图解决的核心瓶颈是：当合成语音达到人类水平时，主观评估（MOS/CMOS/SMOS）资源密集且不可比较，而现有客观指标在跨域和跨语言场景下的相关性表现不一致，难以可靠地区分高质量系统。这一困境的根源在于，大多数客观指标要么是单一维度的信号保真度度量，要么是黑箱预测网络，缺乏对感知因子的显式建模，导致它们在未见域上的泛化能力脆弱。

### 方法谱系：从分布相似性到因子化解构

TTSDS2 的谱系直接继承自 **TTSDS**（Minixhofer et al., 2024），后者首次将 TTS 评估框架定义为分布相似性问题——通过 Wasserstein 距离比较合成语音与真实参考、噪声参考在多个感知因子上的分布差异，并将其归一化为 0–100 的评分。TTSDS2 保留了这一核心框架，但对其三个关键感知因子进行了重构，以提升跨域和跨语言的鲁棒性：

- **INTELLIGIBILITY 特征**：从 TTSDS 的 Word Error Rate（WER）替换为 ASR 模型（whisper, wav2vec 2.0）的最终层激活。这一改变的本质是将可懂度评估从离散的文本对齐错误转化为连续的隐空间分布距离，使其对合成语音中细微的发音退化更敏感。
- **PROSODY 特征**：TTSDS 使用 HuBERT token 长度作为韵律代理，但作者发现该特征会导致低分偏差。TTSDS2 替换为 HuBERT 和 Allosaurus 的去重 token 说话速率，在话语级别捕捉节奏和停顿模式，更直接地反映韵律的自然度。
- **GENERIC 特征**：在 TTSDS 已有的 HuBERT 和 wav2vec 2.0 基础上，增加 WavLM 以提升特征多样性，增强对通用语音质量的覆盖。

最终 TTSDS2 分数是所有因子分数的简单算术平均，这一无监督聚合策略是该方法泛化能力的关键——后续消融实验证明，简单平均在留一法交叉验证中优于通过线性回归学习到的权重（Table 4）。

### 与基线方法的关系

在客观指标谱系中，TTSDS2 的对比基线可分为三类：

1. **MOS 预测网络**：**UTMOS**（Saeki et al., 2022）、**UTMOSv2**（Baba et al., 2024）、**NISQA**（Mittag et al., 2021）、**DNSMOS**（Reddy et al., 2022）和 **SQUIM MOS**（Kumar et al., 2023）。这些方法通过监督学习直接预测人类评分，在训练域内通常表现良好，但在跨域泛化时容易出现聚类行为（Figure 2 中 SQUIM MOS 的散点图显示了明显的域间分离），表明它们学到了与域相关的捷径而非通用的感知质量表征。

2. **分布相似性指标**：**FAD**（Fréchet Audio Distance, Kilgour et al., 2019）与 TTSDS2 共享分布比较的思想，但 FAD 使用单一嵌入空间，缺乏对可懂度、说话人相似性和韵律的显式因子化，使其在细粒度质量区分上不如 TTSDS2。

3. **信号基参考指标**：**MCD**（Mel Cepstral Distortion）、**PESQ**、**STOI** 等传统指标依赖对齐的参考信号，无法处理合成语音与真实语音之间不存在样本级对齐的典型场景，在高质量 TTS 评估中相关性极低。

### 适用边界与局限

TTSDS2 的设计存在明确的适用边界：

- **短句评估**：当前实现仅适用于 3–30 秒的短句，无法评估长篇语音的连贯性、风格适应性或段落级自然度。这是 Wasserstein 距离计算依赖固定长度特征分布的内在限制。
- **计算开销**：每次评估约需 9.4 分钟的 CPU 时间，使其不适合大规模实时基准测试。作者已将探索最大均值差异（MMD）等替代指标作为开放问题。
- **归一化依赖**：TTSDS2 的 0–100 评分依赖于噪声参考和真实参考的 Wasserstein 距离比值。当更强系统持续涌现、合成语音分布进一步逼近真实分布时，该归一化是否仍能保持足够的区分度尚待验证。
- **语言覆盖**：尽管已扩展到 14 种语言，但多语言模型仍以英语为中心，非英语语言的评估可能不够全面。TTSDS2 分数与语言类型学距离的相关性（ρ = -0.51, Section 4.2）表明，语言偏差尚未完全消除。

### 开放问题

1. 能否使用最大均值差异（MMD）等计算更高效的分布距离替代 Wasserstein 距离，使 TTSDS2 适用于大规模基准测试？
2. 如何将因子化分布评估框架扩展到长上下文或长文本的语音评估，捕捉段落级的连贯性和风格一致性？
3. 当合成语音质量持续提升时，当前基于噪声参考的归一化方案是否需要引入更高质量的锚点以维持区分度？
4. 如何将基准评估扩展到更广泛的语言，特别是低资源语言，避免以英语为中心的评价偏差？

## 原文 PDF

![[paperPDFs/ICLR_2026/TTSDS2_Resources_and_Benchmark_for_Evaluating_Human_Quality_Text_to_Speech_Systems.pdf]]

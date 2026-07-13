---
title: "FoleyDesigner: Immersive Stereo Foley Generation with Precise Spatio-Temporal Alignment for Film Clips"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/FoleyDesigner_Immersive_Stereo_Foley_Generation_with_Precise_Spatio_Temporal_Alignment_for_Film_Clips.pdf
project_link: "https://gekiii996.github.io/FoleyDesigner/"
code_link: null
aliases:
- FoleyDesigner
tags:
- CVPR_2026
- topic/generative_models_diffusion
- topic/representation_self_supervised_transfer
- topic/generative_models_diffusion/diffusion_image_video
core_operator: 从视频帧中提取深度和方位角的时空线索（spatio-temporal cues），并通过位置感知的交叉注意力注入扩散Transformer，使生成模型获得帧级别的声音空间位置和激活时刻的显式控制能力。
primary_logic: 将专业拟音工作的三级流程（细粒度的场景事件分解、分轨的时空条件生成、多智能体诊断与混音精修）自动化，同时辅以首个同时带有时间戳和空间标注的立体声拟音数据集FilmStereo，实现端到端的电影级5.1环绕声输出。
claims:
- 时空对齐指标IoU达到32.2，比最佳基线SpatialSonic提升15.8%；空间精度GCC (48.79)和CRW (34.23)均为最优。
- 电影拟音质量ImageBind Score (0.402)比SpatialSonic高60.2%，AV-Sync (0.726)提升33.2%。
- 去除时空条件（STC）后，GCC下降21.3%，CRW下降38.8%，FAD恶化12.1%，验证空间-时间控制对生成质量的关键作用。
- 多智能体精炼框架使事件召回率（ER）从68.5%提升至84.2%，对数谱距离（LSD）和响度误差（LE）大幅降低。
---

# FoleyDesigner: Immersive Stereo Foley Generation with Precise Spatio-Temporal Alignment for Film Clips

> [!tip] 核心洞察
> 将专业拟音工作的三级流程（细粒度的场景事件分解、分轨的时空条件生成、多智能体诊断与混音精修）自动化，同时辅以首个同时带有时间戳和空间标注的立体声拟音数据集FilmStereo，实现端到端的电影级5.1环绕声输出。

| 字段 | 内容 |
|------|------|
| 中文题名 | FoleyDesigner：面向电影剪辑的沉浸式立体声拟音生成，具有精确时空对齐 |
| 英文题名 | FoleyDesigner: Immersive Stereo Foley Generation with Precise Spatio-Temporal Alignment for Film Clips |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2604.05731) · [Project](https://gekiii996.github.io/FoleyDesigner/) |
| Topic | #topic/generative_models_diffusion #topic/representation_self_supervised_transfer #topic/generative_models_diffusion/diffusion_image_video |
| Method | FoleyDesigner |
| Dataset | FilmStereo, Film Clips |

> [!tip] 效果简介
> - FilmStereo 上，FAD (↓) 1.88 vs 2.37 (Stable Audio) (-20.7%)；CLAP (↑) 0.679 vs 0.672 (SpatialSonic) (+1.0%)；IoU (↑) 32.2 vs 27.8 (SpatialSonic) (+15.8%)。
> - Film Clips 上，ImageBind Score (↑) 0.402 vs 0.251 (SpatialSonic) (+60.2%)；AV-Sync (↑) 0.726 vs 0.545 (SpatialSonic) (+33.2%)。

## 概要

电影拟音（Foley）是影视后期制作中为无声画面同步添加音效的关键环节，专业拟音师需要精确控制每个声音事件的空间位置、激活时刻和声学特性，最终输出多声道环绕声。然而，现有音频生成方法面临一个核心瓶颈：**文本或图像条件缺乏精确的空间轨迹描述，视频条件方法多为单声道且无法动态追踪声源移动**，导致生成结果无法融入专业影视后期制作流程。

FoleyDesigner 的核心洞察在于将专业拟音工作的三级流程自动化——**细粒度的场景事件分解、分轨的时空条件生成、多智能体诊断与混音精修**。具体而言，该方法从视频帧中提取深度和方位角的时空线索（spatio-temporal cues），通过位置感知的交叉注意力注入扩散 Transformer（DiT），使生成模型获得帧级别的声音空间位置和激活时刻的显式控制能力。同时，该工作构建了首个同时带有时间戳和空间标注的立体声拟音数据集 **FilmStereo**，为端到端的电影级 5.1 环绕声输出提供了训练基础。

实验结果表明，FoleyDesigner 在时空对齐指标上显著优于现有方法：IoU 达到 32.2，比最佳基线 SpatialSonic 提升 15.8%；空间精度 GCC（48.79）和 CRW（34.23）均为最优。在电影级拟音质量上，ImageBind Score（0.402）比 SpatialSonic 高 60.2%，AV-Sync（0.726）提升 33.2%。消融实验进一步验证了时空条件的关键作用——去除时空条件后，GCC 恶化 21.3%，CRW 恶化 38.8%，FAD 恶化 12.1%。多智能体精炼框架使事件召回率从 68.5% 提升至 84.2%，频谱清晰度和响度平衡也获得显著改善。

在方法谱系上，FoleyDesigner 区别于以文本/图像为条件的立体声生成方法（如 **Stable Audio Open**、**SpatialSonic**、**See2Sound**），以及单声道拟音方法（如 **Diff-Foley**、**FoleyCrafter**），首次实现了帧级时空对齐的立体声拟音，并完整覆盖从脚本分解到专业混音的全流程。

电影后期音频制作中，拟音（Foley）是将视觉叙事转化为听觉沉浸感的关键环节。专业拟音师需要在录音棚中实时观看画面，同步执行脚步声、衣物摩擦、道具碰撞等声音表演，并通过多轨录音、空间声像定位和精细混音，最终输出与画面精确同步的立体声乃至环绕声音轨。这一流程高度依赖人工经验，耗时巨大，且难以规模化。

近年来，生成式音频模型取得了显著进展，但在电影级拟音场景中仍存在三个核心缺口：

**1. 空间定位缺失。** 现有方法主要依赖文本或图像条件生成音频（如 **Stable Audio Open** 和 **SpatialSonic**），缺乏对声源在三维空间中位置和运动轨迹的显式建模。文本描述无法精确传达“从左侧快速移动到右侧”的空间轨迹，导致生成结果的空间感与画面脱节，无法满足专业影视对声像定位的要求。

**2. 帧级时序同步不足。** 视频条件方法（如 **Diff-Foley** 和 **FoleyCrafter**）虽能捕捉一定的音画关联，但多为单声道生成，且无法在帧级别精确控制声音事件的激活时刻。画面中爆炸、击打等瞬态事件需要毫秒级的音画同步，现有方法常出现时序错位，无法融入专业后期制作流程。

**3. 缺乏系统化的拟音流程建模。** 专业拟音工作遵循“场景分解—分轨录制—诊断精修—混音输出”的多级流程，而现有方法多为端到端的单阶段生成，缺乏对声音事件层次化分解、分轨空间控制和后期精修的完整建模，导致生成结果在事件完整性、声学真实感和混音平衡等方面存在明显不足。

上述缺口的根本瓶颈在于：**现有音频生成范式无法同时满足立体声空间定位和帧级时序同步的双重约束**。这促使本文提出 FoleyDesigner，通过模拟专业拟音师的三级工作流，将细粒度场景分解、时空条件生成和多智能体精炼融为一体，实现端到端的电影级立体声拟音。

## 核心方法与创新机理

FoleyDesigner 的核心创新并非单一技术点的突破，而是将专业拟音师的三级工作流（细粒度场景分解 → 分轨时空条件生成 → 多智能体诊断与混音精修）完整自动化，并辅以首个同时带有时间戳和空间标注的立体声拟音数据集 **FilmStereo**，从而在电影级 5.1 环绕声输出上实现了端到端的可控生成。其相对于现有方法的本质差异体现在三个关键维度的 **changed slots** 上。

### 条件控制方式：从语义嵌入到显式时空轨迹

现有音频生成方法（如 **Stable Audio Open**、**SpatialSonic**、**See2Sound**）的条件信号主要依赖文本或图像的全局语义嵌入，缺乏对声源空间位置和激活时刻的精确描述能力。这导致生成结果虽然语义相关，但无法实现“声音跟随画面物体移动”的电影级同步效果。

FoleyDesigner 的核心因果调节旋钮在于：**从视频帧中提取深度和方位角的时空线索，并通过位置感知的交叉注意力注入扩散 Transformer（DiT）**。具体而言，系统利用视觉跟踪模型对每一帧的目标边界框进行定位，结合深度估计计算方位角：

$$\theta_i = \arctan \left( \frac{x_i - W/2}{d_i} \right) \cdot \frac{180^\circ}{\pi} + 90^\circ$$

同时引入帧级激活掩码，仅在声音事件发生的时刻保留有效位置信息，形成时间对齐的空间轨迹：

$$\mathbf{p}_t = c_t \cdot \mathbf{x}_t, \quad \mathcal{P} = \{\mathbf{p}_t\}_{t=1}^{T}$$

这些稀疏的位置序列经过傅立叶特征变换和卷积编码器压缩后，在 DiT 的选定层（第 3、7、11、15、19、23 层）通过交叉注意力融合到音频潜变量中，使生成模型获得了帧级别的声音空间位置和激活时刻的显式控制能力。消融实验（Table 4）表明，**去除时空条件（w/o STC）后，空间精度指标 GCC 恶化 21.3%、CRW 恶化 38.8%，生成质量 FAD 恶化 12.1%**，直接验证了这一控制机制对生成质量的关键作用。

### 场景分解策略：从整体生成到层次化拟音脚本

传统方法通常将视频到音频视为整体映射问题，无法处理声音事件的重叠与分层（如前景脚步声与背景环境声同时存在）。FoleyDesigner 引入了基于 **Tree-of-Thought（ToT）推理的多智能体分解与验证机制**，将无声视频分解为带有前/背景层标记的层次化拟音脚本。生成器与验证器形成闭环迭代：

$$\mathcal{T}^{(k+1)} = \mathrm{Generator}(\mathcal{V}, \mathrm{Feedback}(\mathcal{T}^{(k)}, \mathcal{V}))$$

通过分支探索、剪枝保留 top-k 候选，以及基于视觉-音频对齐度、层次分离度和情感一致性的评分函数进行路径选择，最终产出结构化的多轨拟音脚本。这一分解策略使得后续的时空生成模块可以对每个声音事件独立施加精确的空间控制，而无需处理复杂的声源分离问题。

### 后处理与混音：从简单线性混合到多智能体精修

现有方法在生成后通常仅做简单的线性混合，缺乏专业的后期处理。FoleyDesigner 模拟专业拟音团队的协作框架，构建了**分析-规划-执行的多智能体混音精炼框架**：诊断智能体识别频谱缺陷、混响偏差和动态失衡，规划智能体制定修正策略，执行智能体分别调整混响、均衡和动态参数，最终通过 120Hz 低通滤波生成 LFE 通道并上混为 5.1 环绕声。消融实验（Table 5）显示，**多智能体精炼使事件召回率（ER）从 68.5% 提升至 84.2%，对数谱距离（LSD）和响度误差（LE）大幅降低**，验证了后期精修对电影级输出质量的重要性。

### 数据集贡献：FilmStereo

上述创新的实现依赖于 **FilmStereo** 数据集——首个同时带有时间戳和空间标注的立体声拟音数据集。其构建流程包括音频过滤与扩展、随机空间定位模拟、基于思维链的空间丰富描述生成，以及事件检测的时间标注四个步骤，覆盖 8 类常见音效。这一数据集填补了现有立体声拟音数据缺乏精确时空标注的空白，为时空对齐模型的训练和评估提供了基准。

> **需要手动验证**：FoleyDesigner 在推理延迟方面存在明显局限——生成 3 秒立体声片段总耗时约 108 秒（单张 A6000 GPU），尚无法满足实时交互需求。此外，多目标跟踪能力有限，当前主要针对单一声源的空间定位，密集重叠并发事件的分离与定位仍是开放问题。

FoleyDesigner 将专业拟音师的工作流程抽象为三个顺序衔接的功能模块，形成端到端的自动化拟音管线。如图 1 所示，该管线模拟了人工拟音从场景理解、分轨录制到后期混音的全过程，最终输出可直接用于电影制作的 5.1 环绕声音轨。

### 三级流水线架构

系统的核心架构由以下三个阶段构成（图 2）：

1. **细粒度影片分解**：以无声视频为输入，利用视觉语言模型和思维树推理，将影片内容分解为层次化的拟音脚本。脚本明确指定了前景层与背景层的多个声音事件，每个事件附带视觉描述、时序边界和声源类型。

2. **时空拟音生成**：针对脚本中的每个声音事件，从视频帧中提取深度和方位角的时空线索，通过基于 DiT 的潜在扩散模型进行条件生成。该阶段实现了帧级别的空间定位与激活时刻的精确控制，输出分轨的立体声音频。

3. **拟音精炼与专业混音**：多智能体框架对生成的分轨音频进行诊断，识别并修正混响、均衡和动态等声学缺陷，最终将各轨混合并上混为 5.1 声道环绕声输出。

### 输入输出流

整个管线的信息流可概括为：

- **输入**：无声电影视频片段。
- **中间产物**：层次化拟音脚本 → 带时空标注的分轨立体声音频。
- **输出**：经多智能体精炼的 5.1 声道环绕声音轨，包含左、中、右、左环绕、右环绕和低频效果通道。

### 关键创新点

与现有方法相比，FoleyDesigner 的核心差异在于：

- **显式时空控制**：不同于纯文本或图像嵌入的条件方式，本方法从视频帧中提取深度和方位角，通过傅立叶特征编码和位置感知交叉注意力注入扩散 Transformer，使模型获得帧级别的声源空间位置和激活时刻的显式控制能力。
- **层次化场景分解**：采用基于思维树的多智能体分解与验证机制，替代整体生成策略，能够处理声音事件的重叠与分层。
- **专业后期处理**：引入多智能体分析-规划-执行的混音精炼框架，模拟专业拟音团队的协作流程，而非简单的线性混合。

### 数据支撑

为训练和评估上述管线，作者构建了 **FilmStereo** 数据集——首个同时带有时间戳和空间标注的立体声拟音数据集。其构建流程（图 3）包括音频过滤与扩展、随机定位的空间模拟、基于思维链的空间丰富描述生成，以及事件检测的时间标注四个步骤。

![[assets/figures/papers/paper_list_l2489_https_arxiv_org_abs_2604_05731/figures/001_Figure_1.jpg]]
*Figure 1: FoleyDesigner Overview. The left column detailing the actual steps of a human Foley designer. The right column presents the corresponding simulated functional modules of FoleyDesigner, showcasing outputs at each phase, resulting in a soundtrack suitable for film use*

![[assets/figures/papers/paper_list_l2489_https_arxiv_org_abs_2604_05731/figures/012_Figure_1.jpg]]
*Figure 1: FilmStereo Dataset Pipeline. The process begins with sourcing data using randomly sampled parameters to define sound event attributes, followed by a simulated sound design scenario in Step 2 to generate film foley annotations. The resulting data undergoes manual verification to ensure quality and accuracy*

FoleyDesigner 将专业拟音工作流抽象为三个序贯阶段：**细粒度影片分解**、**时空拟音生成**与**拟音精炼与专业混音**。本节聚焦前两个阶段的核心公式与关键模块，精炼阶段的混音公式见 Eq. (8)。

### 细粒度影片分解：Tree-of-Thought 脚本生成

该阶段由 **FilmScribe** 模块实现，其目标是将无声视频 $\mathcal{V}$ 转化为结构化的层次化拟音脚本 $\mathcal{T}$，包含视觉描述与声音事件规格。核心机制是**生成器-验证器闭环迭代**：

$$\mathcal{T}^{(k+1)} = \mathrm{Generator}(\mathcal{V}, \mathrm{Feedback}(\mathcal{T}^{(k)}, \mathcal{V}))$$

生成器根据视频与上一轮反馈生成候选脚本，验证器评估其准确性并输出反馈，迭代直至收敛。

为处理复杂场景中多事件的层次关系，引入 **Tree-of-Thought (ToT)** 推理。对候选脚本 $\mathcal{S}$，其质量由三维评分函数量化：

$$\mathrm{Score}(\mathcal{S}, \mathcal{V}, \mathcal{F}) = w_{1} s_{\mathrm{align}} + w_{2} s_{\mathrm{layer}} + w_{3} s_{\mathrm{emotion}}$$

其中 $s_{\mathrm{align}}$ 衡量视听对齐度，$s_{\mathrm{layer}}$ 评估前景/背景层分离的合理性，$s_{\mathrm{emotion}}$ 度量情感一致性。搜索过程通过剪枝保留每层 top-k 候选，终止条件为 Score 超过阈值 $\tau$、深度超出 $d_{\max}$ 或分支预算耗尽。

### 时空拟音生成：位置感知交叉注意力注入

该阶段是 FoleyDesigner 实现帧精确空间控制的核心。其因果旋钮在于：从视频帧中提取**深度与方位角的时空轨迹**，通过傅立叶特征编码与位置感知交叉注意力注入扩散 Transformer (DiT)，使生成模型获得帧级声音空间位置与激活时刻的显式控制。

#### 时空线索提取

对第 $i$ 个声音事件，从视频帧的边界框与深度估计中计算逐帧空间位置。**方位角**由边界框水平中心 $x_i$ 与深度 $d_i$ 映射到 $[0^\circ, 180^\circ]$ 空间：

$$\theta_i = \arctan \left( \frac{x_i - W/2}{d_i} \right) \cdot \frac{180^\circ}{\pi} + 90^\circ$$

其中 $W$ 为帧宽。将深度与方位角组合为位置向量 $\mathbf{x}_t$，乘以帧级**激活掩码** $c_t \in \{0, 1\}$（由事件检测确定该帧是否有声），形成时间对齐的空间轨迹：

$$\mathbf{p}_t = c_t \cdot \mathbf{x}_t, \quad \mathcal{P} = \{\mathbf{p}_t\}_{t=1}^{T}$$

#### 傅立叶特征编码

稀疏的位置序列需增强表达能力。采用随机傅立叶特征映射将低维 $\mathbf{p}_t$ 投影到高维空间：

$$\gamma(\mathbf{p}_t) = [ \cos(2\pi \mathbf{B} \mathbf{p}_t); \sin(2\pi \mathbf{B} \mathbf{p}_t) ] \in \mathbb{R}^{2m}$$

其中 $\mathbf{B} \in \mathbb{R}^{m \times d}$ 为随机高斯矩阵。为在非活跃帧保留微弱位置记忆以实现平滑空间连续性，引入**调制特征**：

$$\tilde{\gamma}(\mathbf{p}_t) = c_t \cdot \gamma(\mathbf{p}_t) + \epsilon \cdot \gamma(\mathbf{p}_t), \quad \epsilon=0.1$$

调制后的序列经卷积编码器压缩到与音频潜变量相同的时间尺度：

$$\mathbf{E}_{\mathrm{pos}} = \mathrm{PosEncoder}(\{\tilde{\gamma}(\mathbf{p}_t)\}_{t=1}^{T}) \in \mathbb{R}^{T' \times d_{\mathrm{emb}}}$$

#### 交叉注意力注入

位置嵌入在 DiT 的选定层通过交叉注意力融合到潜在特征中。注入模块插入在每 4 个标准 DiT 块之后，具体位于层 $\ell \in \{3, 7, 11, 15, 19, 23\}$：

$$\mathbf{z}_{\ell}^{\prime} = \mathrm{InjBlock}(\mathbf{z}_{\ell}, \mathrm{LN}(\mathbf{E}_{\mathrm{pos}}))$$

其中 $\mathbf{z}_{\ell}$ 为第 $\ell$ 层潜在特征，$\mathrm{LN}$ 为层归一化。该设计使模型在去噪过程中持续感知声源的帧级空间位置，是实现 IoU 达 32.2（Table 2）的关键。

![[assets/figures/papers/paper_list_l2489_https_arxiv_org_abs_2604_05731/figures/010_Table_2.jpg]]
*Table 2: Percentage distribution. The table shows the proportion of audio clips belonging to each of the eight major sound design categories*

### 5.1 声道上混

精炼后的立体声混音通过低通滤波生成低频效果通道（LFE），完成 5.1 环绕声输出：

$$\mathbf{s}_{\mathrm{LFE}}(t) = \mathrm{LPF}(\mathbf{s}_{\mathrm{mix}}(t), 120\mathrm{Hz})$$

### 消融验证

去除时空条件（w/o STC）导致 GCC 恶化 21.3%、CRW 恶化 38.8%、FAD 恶化 12.1%（Table 4），直接验证了上述时空注入机制对空间精度与生成质量的决定性作用。多智能体精炼框架使事件召回率从 68.5% 提升至 84.2%（Table 5），印证了三级流水线的协同增益。

## 实验与关键发现

FoleyDesigner 在音频质量、时空对齐、电影级拟音性能及人类主观偏好等多个维度上均展现出对现有基线方法的显著优势，并通过系统的消融实验验证了各核心模块的必要性。

### 音频质量评估

在 FilmStereo 数据集上的客观质量评估（Table 1）显示，FoleyDesigner 在 Fréchet Audio Distance (FAD) 指标上达到 **1.88**，较最佳基线 Stable Audio Open 的 2.37 降低了 20.7%，表明其生成音频的分布与真实拟音录音高度吻合。在语义对齐指标 CLAP 上，FoleyDesigner 取得 **0.679** 的最优分数，略优于 SpatialSonic (0.672)，说明其生成的立体声音频与视频内容的语义一致性更强。值得注意的是，Inception Score 和 KL Divergence 等指标上各方法差距较小，这反映了当前立体声生成模型在基础声学质量上已趋于接近，而 FoleyDesigner 的核心优势在于后续的时空控制精度。

![[assets/figures/papers/paper_list_l2489_https_arxiv_org_abs_2604_05731/figures/004_Table_1.jpg]]
*Table 1: Audio Quality. Metrics include Inception Score, KL Divergence, Frechet Audio Distance, and CLAP score for audio ´ quality assessment. Best and second-best results are highlighted. ↓ indicates lower is better, ↑ indicates higher is better*

### 时空对齐精度

时空对齐是 FoleyDesigner 的核心设计目标。Table 2 的结果显示，FoleyDesigner 在空间精度指标上全面领先：GCC 达到 **48.79**（越低越好），较 SpatialSonic 的 59.24 降低 17.6%；CRW 为 **34.23**，较 SpatialSonic 的 56.12 降低 39.0%。在时间对齐指标 IoU 上，FoleyDesigner 取得 **32.2**，比 SpatialSonic 提升 15.8%。这一优势源于从视频帧中显式提取的深度-方位角时空线索，通过位置感知交叉注意力直接注入扩散 Transformer 的生成过程，使模型获得了帧级别的声源定位能力。

![[assets/figures/papers/paper_list_l2489_https_arxiv_org_abs_2604_05731/figures/006_Table_2.jpg]]
*Table 2: Spatio-Temporal Alignment Results. Metrics include GCC and CRW for spatial accuracy, FSAD for stereo quality, and IoU for temporal alignment. Best and second-best results are highlighted. ↓ indicates lower is better, ↑ indicates higher is better*

定性分析（Figure 6, Figure 7, Figure 8）进一步印证了这一结论：在爆炸序列中，FoleyDesigner 的频谱能量与三个关键事件帧精确对齐，而基线方法普遍存在时间错位；在声像移动场景中，FoleyDesigner 的左右声道能量随声源位置变化呈现清晰的此消彼长，而 SpatialSonic 尽管输出双声道，却缺乏明显的空间变化。

### 电影级拟音性能

在真实电影剪辑上的评估（Table 3）揭示了 FoleyDesigner 在专业影视场景中的实用价值。ImageBind Score 达到 **0.402**，比 SpatialSonic 的 0.251 高出 60.2%，表明其生成的音效与视觉内容的跨模态一致性远超现有方法。AV-Sync 指标为 **0.726**，较 SpatialSonic 提升 33.2%，验证了帧级同步的有效性。在电影质感维度上，Sonic Richness Score 和 Cinematic Clarity Score 均为最优，这与 FoleyDesigner 模拟专业拟音师三级流程（分解-生成-精修）的设计理念一致。

人类主观评测（Figure 5）提供了最直接的体验证据：在沉浸感（Immerse）、情感对齐（Emo Align）、节奏对齐（Tempo Align）、空间对齐（Spatial Align）和音色（Timbre）五个维度上，FoleyDesigner 的偏好选择率均显著高于基线方法（卡方检验 p < 0.001）。尤其在空间对齐维度上，FoleyDesigner 的选择率超过 60%，而 SpatialSonic 不足 20%，直接反映了时空注入机制对主观听感的决定性影响。

### 消融实验

消融实验验证了两个关键设计的作用：

**时空条件注入（STC）的消融**（Table 4）：移除时空条件后，空间精度指标 GCC 从 48.79 恶化至 62.02（下降 21.3%），CRW 从 34.23 恶化至 55.89（下降 38.8%），同时 FAD 从 1.88 升至 2.14（恶化 12.1%）。这表明时空线索不仅控制空间定位，还对生成音频的整体质量有正向贡献——位置信息为扩散模型提供了额外的条件约束，减少了生成过程中的歧义。

**多智能体精炼框架的消融**（Table 5）：单阶段生成（无多智能体精炼）的事件召回率（ER）仅为 68.5%，而完整框架达到 **84.2%**，提升 15.7 个百分点。同时，对数谱距离（LSD）和响度误差（LE）大幅降低，RT60 混响时间误差（RT60E）也有明显改善。这说明多智能体诊断-规划-执行的闭环精修能有效捕捉并纠正单次生成中的遗漏事件和声学缺陷，是保证电影级输出完整性的关键环节。

### 推理效率与扩展基线

推理时间分析（Table 3 Supp）显示，生成 3 秒立体声片段总耗时约 108 秒，其中分解阶段约 15 秒，生成阶段约 75 秒，精炼阶段约 18 秒。这一延迟尚无法满足实时交互需求，是当前方法的主要工程瓶颈。

在扩展基线对比（Table 4 Supp）中，FoleyDesigner 同样优于单声道拟音方法 Diff-Foley 和 FoleyCrafter，进一步验证了立体声空间控制对电影级拟音的必要性——单纯提升单声道生成质量无法弥补空间定位的缺失。

![[assets/figures/papers/paper_list_l2489_https_arxiv_org_abs_2604_05731/figures/009_Table_4.jpg]]
*Table 4: Ablation study results on the FilmStereo dataset. STC refers to spatio-temporal cues including trajectory information and spatial positioning prompts. Best results are highlighted*

### 失败模式与局限性

尽管整体表现优异，FoleyDesigner 仍存在以下可观察的失败模式：

1. **多声源重叠场景**：当前时空线索提取主要针对单一声源的边界框，当多个声源在空间中密集重叠时，模型倾向于生成主导声源而忽略次要事件，导致事件召回率下降。
2. **视觉信息不足场景**：混响等声学参数的估计依赖视觉空间线索，在黑暗、烟雾或快速切换镜头中，深度估计和方位角计算存在偏差，导致空间定位失准。
3. **数据集覆盖范围**：FilmStereo 仅覆盖 8 类常见音效（Table 2 Supp），对于数据集外的声音类别（如特殊机械、自然现象），模型的泛化能力尚待验证。

## 定位与知识库关联

### 与现有基线的关系

FoleyDesigner 的提出直接回应了当前音频生成领域的一个结构性缺口：**立体声空间定位与帧级时序同步的分离**。现有方法大致可分为三类，每一类在特定维度上与 FoleyDesigner 形成对比或互补。

**文本/图像条件的立体声生成方法**，如 **Stable Audio Open** 和 **SpatialSonic**，能够产生双声道输出并具备一定的空间感，但其条件控制依赖于文本描述或静态图像嵌入，缺乏对声源运动轨迹和激活时刻的显式建模。SpatialSonic 在空间精度指标上已是基线中最优（IoU 27.8，Table 2），但 FoleyDesigner 通过将深度-方位角时空线索注入扩散 Transformer，将 IoU 提升至 32.2（+15.8%），GCC 从 52.31 降至 48.79（↓表示更优）。**See2Sound** 同样属于图像到立体声的生成范式，但完全缺失时间维度，无法处理动态场景中的声像移动。

**视频条件的单声道拟音方法**，如 **Diff-Foley** 和 **FoleyCrafter**，在生成质量上表现不俗，但输出为单声道，不具备空间定位能力。FoleyCrafter 在补充实验（Supp Table 4）中被纳入对比，其在 FAD 指标上为 2.04，弱于 FoleyDesigner 的 1.88，且无法评估 GCC、CRW 等空间指标。这类方法的核心局限在于：即使生成内容与视频语义对齐，也无法为后期制作提供可用的立体声素材。

**端到端视频到音频生成方法**在近年快速发展，但多数聚焦于单声道环境声或通用音效，未将拟音工作的专业流程（事件分解、分轨生成、混音精修）纳入设计。FoleyDesigner 的独特贡献在于将这一三级流水线自动化，并通过首个带有时间戳和空间标注的立体声拟音数据集 **FilmStereo** 提供训练支撑。

从方法演进的角度看，FoleyDesigner 在以下三个关键维度上重新定义了视频条件音频生成的技术边界：

| 维度 | 基线方法特征 | FoleyDesigner 创新 |
|------|-------------|-------------------|
| 条件控制方式 | 纯文本或图像嵌入，缺乏显式时空定位 | 从视频帧提取深度、方位角和帧级激活掩码，通过傅立叶特征编码和位置感知交叉注意力注入 DiT |
| 场景分解策略 | 整体生成，无法处理声音事件重叠 | 基于 Tree-of-Thought 的多智能体分解与验证，产生层次化拟音脚本 |
| 后处理与混音 | 无专业后期处理或仅简单线性混合 | 多智能体分析-规划-执行的混音精炼框架，支持 5.1 声道上混 |

### 适用边界与局限

尽管 FoleyDesigner 在 FilmStereo 数据集和电影片段评估上取得了显著优势，其适用边界受以下因素制约：

1. **推理延迟**：生成 3 秒立体声片段总耗时约 108 秒（Supp Table 3），远未达到实时交互需求。三级流水线中，时空拟音生成阶段占主要耗时，限制了其在直播、实时配音等场景的应用。

2. **多目标跟踪能力有限**：当前框架主要针对单一声源的空间定位。在多个声源同时移动或密集重叠的场景中（如群战场面），视觉跟踪模块难以准确分离并分配各自的时空轨迹。论文将此列为开放问题，但未给出具体改进方案。

3. **声学参数估计依赖视觉信息**：混响时间（RT60）等声学参数的估计完全依赖视频帧中的场景线索。在视觉信息不足的开放场景（如纯黑背景、快速镜头切换）中，混响估计存在偏差，可能导致空间感不自然。消融实验（Table 5）显示，去除多智能体精炼框架后，RT60 误差显著增大。

4. **数据集覆盖范围有限**：FilmStereo 数据集仅覆盖 8 类常见音效（如爆炸、脚步、引擎等，Supp Table 2），泛化到更广泛的电影场景（如自然声景、科幻音效、音乐性拟音）仍待验证。数据集的构建依赖空间模拟和随机定位，可能无法完全还原真实录制中的声学特性。

5. **5.1 声道上混的简化处理**：LFE 声道通过简单低通滤波生成（$f_c=120\text{Hz}$），环绕声道由立体声上混得到，未对后置声道的独立空间信息进行建模。在需要精确环绕声定位的场景中，这种简化可能影响沉浸感。

### 开放问题与后续方向

论文明确指出了若干待解决的问题，这些方向也构成了该领域的潜在研究热点：

- **密集并发事件处理**：如何高效处理多个同时发生且空间位置不同的声音事件？可能的路径包括引入声源分离模块或多通道并行生成架构。
- **多目标跟踪与分离**：当前框架的视觉跟踪模块尚不能同时追踪多个独立声源，改进计划未在论文中详述，但这是实现复杂场景拟音的关键前提。
- **声道格式扩展**：能否将框架扩展到 7.1.4 乃至全景声（如 Dolby Atmos）格式？这需要在空间编码和上混策略上进行根本性改进。
- **推理延迟优化**：在保证质量的前提下大幅降低推理延迟，是推动该方法走向实际影视制作流程的必要条件。可能的路径包括模型蒸馏、流式生成或高效注意力机制。
- **跨域泛化**：FilmStereo 的 8 类音效覆盖有限，如何将时空控制能力泛化到更广泛的音效类型和场景，需要更大规模、更多样化的标注数据集支持。

需要手动验证的是：论文未提供与最新视频到音频方法（如 2024-2025 年出现的基于视频扩散模型的生成方法）的直接对比，这可能是由于论文投稿时间与这些方法出现的时间窗口重叠。建议读者在定位本方法时，补充与同期工作的横向比较。

## 原文 PDF

![[paperPDFs/CVPR_2026/FoleyDesigner_Immersive_Stereo_Foley_Generation_with_Precise_Spatio_Temporal_Alignment_for_Film_Clips.pdf]]

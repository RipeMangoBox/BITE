---
title: "EmoTaG: Emotion-Aware Talking Head Synthesis on Gaussian Splatting with Few-Shot Personalization"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/EmoTaG_Emotion_Aware_Talking_Head_Synthesis_on_Gaussian_Splatting_with_Few_Shot_Personalization.pdf
project_link: null
code_link: null
aliases:
- EmoTaG
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 通过将运动预测从直接变形3D高斯转移到预测FLAME表达和下巴姿态参数，引入显式几何先验以提升运动稳定性；同时，设计门控残差运动网络（GRMN）解耦语音运动与情绪调制，并通过语义情绪引导蒸馏情绪知识。
primary_logic: 将运动预测重新形式化为FLAME参数回归，利用FLAME网格的强结构化先验确保一致性；通过GRMN的基分支、残差分支和门控分支实现中性语音与情绪相关运动的自适应融合；并采用教师-学生框架从预训练情绪识别器蒸馏情绪分布和强度，无需人工标注即可实现情绪感知学习。
claims:
- 情绪音频的嘴部运动轨迹波动显著大于中性音频（标准差7.88 vs 3.11），揭示情绪建模的必要性。
- 在自重建任务上，EmoTaG在所有评估指标（PSNR、LPIPS、SSIM、LMD、AUE、Sync-C）上均优于现有最佳方法。
- 消融实验表明，移除语义情绪引导 (SEG) 导致所有指标显著下降，PSNR从29.95降至29.01，证实其关键作用。
- 移除AdaIN身份调制导致最大性能下降（PSNR降至28.38），说明个性化运动风格建模至关重要。
---

# EmoTaG: Emotion-Aware Talking Head Synthesis on Gaussian Splatting with Few-Shot Personalization

> [!tip] 核心洞察
> 将运动预测重新形式化为FLAME参数回归，利用FLAME网格的强结构化先验确保一致性；通过GRMN的基分支、残差分支和门控分支实现中性语音与情绪相关运动的自适应融合；并采用教师-学生框架从预训练情绪识别器蒸馏情绪分布和强度，无需人工标注即可实现情绪感知学习。

| 字段 | 内容 |
|------|------|
| 中文题名 | EmoTaG：基于高斯泼溅的情绪感知说话人头像合成与少样本个性化 |
| 英文题名 | EmoTaG: Emotion-Aware Talking Head Synthesis on Gaussian Splatting with Few-Shot Personalization |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2603.21332) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | EmoTaG |
| Dataset | HDTF, MEAD-derived emotional test set |
> [!tip] 效果简介
> - 自重建 (中性视频, 5s训练数据) 上，PSNR↑ / LPIPS↓ / SSIM↑ / LMD↓ / AUE-(L/U)↓ / Sync-C↑ 30.02 / 0.019 / 0.883 / 2.221 / 0.685 0.210 / 6.212 vs 次优基线 (如InsTaG或MimicTalk) (未提供具体数值差值，但EmoTaG在所有指标上均排名第一)。
> - 自重建 (情绪视频, 5s训练数据) 上，PSNR↑ / LPIPS↓ / SSIM↑ / LMD↓ / AUE-(L/U)↓ / Sync-C↑ 29.95 / 0.022 / 0.877 / 2.456 / 0.702 0.236 / 6.147 vs 次优基线 (EmoTaG领先，具体差值未列出)。

## 概要

**问题瓶颈**：现有少样本3D说话人头像合成方法（如InsTaG、MimicTalk）在情绪驱动场景下面临两个根本性缺陷——几何不稳定与音频-情绪不匹配。如图2所示，情绪音频的嘴部运动轨迹波动显著大于中性音频（水平/垂直标准差分别为7.88/6.92 vs 3.11），揭示情绪语音包含更复杂的发音模式，而现有方法缺乏对这类情绪驱动面部运动的有效建模。

**核心思路**：EmoTaG通过三个关键设计解决上述瓶颈：（1）将运动预测从直接变形3D高斯重新形式化为FLAME表达与下巴姿态参数回归，利用FLAME网格的强结构化先验保证运动几何稳定性；（2）设计门控残差运动网络（GRMN），通过基分支捕捉中性语音运动、残差分支建模情绪相关偏差、门控分支实现自适应融合，解耦语音运动与情绪调制；（3）引入语义情绪引导（SEG），以DeepFace为教师模型蒸馏情绪分布与强度，无需人工标注即可实现情绪感知学习。

**方法定位**：EmoTaG建立在FLAME-Gaussian表示之上，属于“参数化人脸先验+3D高斯泼溅”的技术路线，与InsTaG（Li et al., CVPR 2025）共享FLAME-Gaussian基础框架，但在运动预测范式上做出根本性改变——从直接预测高斯变形转向预测FLAME参数，并通过GRMN实现情绪解耦建模。

**主要结果**：在5秒训练数据的自重建任务上，EmoTaG在PSNR、LPIPS、SSIM、LMD、AUE、Sync-C等全部评估指标上均优于现有最佳方法（Table 1）。消融实验证实，移除语义情绪引导导致PSNR从29.95降至29.01、LMD从2.456升至3.067，而移除AdaIN身份调制造成最大性能降幅（PSNR降至28.38），证明情绪蒸馏与个性化运动风格建模的核心作用（Table 5）。

### 3D说话人头像合成：从几何保真到情绪表达

真实感3D说话人头像合成是计算机视觉与图形学交叉领域的核心挑战，其目标是根据驱动音频生成动态的、视觉逼真的面部动画。近年来，基于3D高斯泼溅（3D Gaussian Splatting, 3DGS）的方法在渲染质量与效率上取得了突破性进展，使得从少量训练数据中重建可驱动的3D头部模型成为可能。然而，现有方法普遍聚焦于中性语音下的唇音同步与视觉保真度，对**情绪感知的3D说话人合成**关注甚少。

### 核心瓶颈：情绪驱动下的几何不稳定与音频-情绪失配

情绪语音对面部运动提出了远高于中性语音的复杂性要求。如Figure 2所示，对唇部关键点轨迹的量化分析揭示了一个关键事实：**情绪音频的嘴部运动轨迹波动显著大于中性音频**——水平与垂直方向的标准差分别为7.88和6.92，而中性音频仅为3.11。这意味着情绪语音包含更复杂的发音模式与更强烈的时序波动，直接对运动预测网络的稳定性构成挑战。

当前少样本3D说话人方法（如**InsTaG**（Li et al., CVPR 2025）、**MimicTalk**（Ye et al., NeurIPS 2024））通常采用直接预测3D高斯变形参数的方式驱动面部动画。这种无约束的运动表示在应对情绪语音时暴露出两个结构性缺陷：

1. **几何不稳定**：缺乏显式3D先验的变形预测容易产生不自然的网格扭曲与时间抖动，尤其在情绪引发的夸张表情下更为明显。
2. **音频-情绪失配**：现有方法的运动预测网络未对情绪信号进行显式建模，导致生成的面部运动与音频中的情绪线索脱节——要么情绪表达不足，要么运动与语音节奏失同步。

### 本文动机：引入显式几何先验与情绪蒸馏

针对上述瓶颈，EmoTaG 提出两条核心设计思路：

- **运动预测的重新形式化**：将运动预测从直接变形3D高斯转变为预测**FLAME参数模型的表达与下巴姿态参数**，利用FLAME网格的强结构化先验约束运动空间，从根本上提升几何稳定性。
- **情绪感知的运动解耦**：设计**门控残差运动网络（Gated Residual Motion Network, GRMN）**，通过基分支捕捉语音中性运动、残差分支建模情绪相关偏差、门控分支实现自适应融合，并引入**语义情绪引导（Semantic Emotion Guidance, SEG）**从预训练情绪识别器蒸馏情绪分布与强度知识，在无需人工标注的条件下实现情绪感知学习。

这一设计使得EmoTaG能够在仅5秒训练视频的少样本设定下，同时实现高质量的情绪表达、唇音同步与视觉真实感。

## 核心方法与创新机理

EmoTaG 的核心创新在于将少样本 3D 说话人头像合成从“直接变形高斯”重新形式化为“FLAME 参数回归”，并通过门控残差运动网络（GRMN）与语义情绪引导（SEG）实现情绪感知的运动生成。以下从瓶颈、因果机制和关键设计三个层面展开。

### 1. 瓶颈洞察：情绪语音下的运动不稳定性

现有少样本 3D 说话人方法（如 **InsTaG** (Li et al., CVPR 2025)、**MimicTalk** (Ye et al., NeurIPS 2024)）通常直接预测 3D 高斯的变形参数，缺乏对情绪驱动面部运动的显式建模。Figure 2 的定量分析揭示了这一问题的根源：情绪音频下嘴部张开轨迹的标准差（水平 7.88，垂直 6.92）显著大于中性音频（3.11），表明情绪语音引入了更复杂的发音模式和更强的时序波动。直接变形范式在面对这种波动时，容易出现几何不稳定和音频-情绪不匹配。

### 2. 因果机制：从直接变形到 FLAME 参数回归

EmoTaG 的核心因果调控手段是将运动预测目标从 3D 高斯变形参数切换为 FLAME 表达参数 $\Psi$ 和下巴姿态参数。这一设计引入了 FLAME 网格的强结构化先验，通过 FLAME-Gaussian 映射（Eq. 7）将预测的参数转化为高斯的全局属性，从而在根本上约束运动的一致性和稳定性。与此形成对比的是，基线方法缺乏这种显式几何约束，导致情绪场景下容易出现扭曲和不准确的面部运动（见 Figure 5 红色矩形标注区域）。

### 3. 关键设计：门控残差运动网络（GRMN）

GRMN 是 EmoTaG 方法创新的核心载体，其设计围绕三个 changed slots 展开：

- **身份条件编码器**：融合音频特征、表情特征和身份特征，通过 AdaIN 调制（Eq. 4-5）注入个性化运动风格。消融实验（Table 5）表明，移除 AdaIN 身份调制导致最大性能降幅——PSNR 从 29.95 降至 28.38，LMD 从 2.456 升至 4.021，Sync-C 从 6.147 降至 4.621，证实个性化运动风格建模的核心作用。

- **专家运动解码器**：由基分支、残差分支和门控分支组成。基分支捕捉语音驱动的中性运动，残差分支建模情绪相关的运动偏差，门控分支通过自适应融合机制（Eq. 6）协调两者。移除门控分支会引入时间不稳定性并削弱音频-运动同步（Table 5）。

- **语义情绪引导（SEG）**：采用教师-学生框架，从预训练情绪识别器 DeepFace 蒸馏情绪分布和强度（Eq. 9），无需人工标注即可指导残差分支和门控分支的学习。消融实验显示，移除 SEG 导致 PSNR 从 29.95 降至 29.01，LMD 从 2.456 升至 3.067，Sync-C 从 6.147 降至 5.541，证实其对情绪表达和音频同步的关键贡献。

### 4. 个性化适应策略

与基线方法的全网络微调不同，EmoTaG 在少样本适应阶段仅微调 AdaIN 调制参数，冻结 GRMN 其余部分。这一设计既保留了预训练阶段学到的通用运动先验，又通过身份条件调制实现了高效的个性化运动风格注入。

> **注意**：关于 GRMN 内部各分支的具体网络结构（如层数、维度）以及 SEG 中蒸馏损失的具体权重配置，原文未提供足够细节，需要手动查阅补充材料或代码仓库进行验证。

EmoTaG 的整体流水线围绕两个核心组件构建：**FLAME-Gaussian 模型**（提供结构化三维先验）与**门控残差运动网络**（GRMN，负责预测动态面部运动）。图3展示了预训练与适应两个阶段的完整架构。

**输入与输出流**：系统以音频特征、表情特征和身份特征作为驱动信号，最终输出由三维高斯泼溅渲染的说话人头像帧。其关键设计在于将运动预测重新形式化为 FLAME 参数回归——GRMN 预测 FLAME 的表情参数和下巴姿态参数，而非直接预测高斯变形，从而利用 FLAME 网格的强结构化先验确保运动几何稳定性。

**模块关系**：
1. **身份条件编码器**（Identity-Conditioned Encoder）首先融合多模态驱动信号。它通过 AdaIN 调制机制将身份特征注入音频和表情特征，实现个性化运动风格的注入：
   $$ \gamma, \beta = \mathrm{MLP}(\mathbf{s}) $$
   $$ \tilde{\mathbf{F}} = \gamma \cdot \mathrm{InstanceNorm}(\mathbf{F}) + \beta $$
   其中 $\mathbf{s}$ 为身份特征，$\gamma$ 和 $\beta$ 分别控制特征的缩放与偏置。

2. **专家运动解码器**（Expert Motion Decoder）包含三个协作分支：
   - **基分支**（Base Branch）：捕捉与语音相关的中性运动模式；
   - **残差分支**（Residual Branch）：建模情绪相关的运动偏差；
   - **门控分支**（Gate Branch）：自适应地融合基运动与残差运动，输出最终运动：
     $$ \delta = \delta_{\mathrm{b}} + g \cdot \delta_{\mathrm{r}} $$
     其中 $\delta_{\mathrm{b}}$ 为基分支输出，$\delta_{\mathrm{r}}$ 为残差分支输出，$g$ 为门控权重。

3. **语义情绪引导**（Semantic Emotion Guidance, SEG）模块（图4）采用教师-学生蒸馏框架：以预训练的 DeepFace 情绪识别器作为教师，提供类别情绪分布与标量情绪强度分数 $e = 1 - p_{\mathrm{emo}}(\mathrm{neutral})$，分别通过 KL 散度损失和分数回归损失指导学生网络的残差分支和门控分支学习。

4. **FLAME-Gaussian 映射**：GRMN 预测的 FLAME 表情和下巴参数驱动 FLAME 网格变形，进而通过重心坐标插值驱动绑定的三维高斯：
   $$ \pmb{\mu}_i = \sum_{j=1}^3 w_{ij} \mathbf{v}_j, \quad \sum w_{ij}=1 $$
   对于口内区域的高斯子集 $\mathcal{G}_{\mathrm{mouth}}$，额外施加网络预测的残差偏移以增强精细口腔动画：
   $$ \pmb{\mu}^* = \pmb{\mu} + \Delta \pmb{\mu}, \quad \pmb{r}^* = \pmb{r} + \Delta \pmb{r}, \quad \pmb{s}^* = \pmb{s} + \Delta \pmb{s} $$

**预训练与适应策略**：预训练阶段在多身份语料上学习通用运动先验（250K 迭代，AdamW 优化器）；适应阶段仅需 5 秒新身份视频，冻结 GRMN 除 AdaIN 调制参数外的所有部分，仅微调身份相关的缩放和偏置参数（20K 迭代），实现高效的少样本个性化。训练总损失为：
$$ \mathcal{L} = \mathcal{L}_{\mathrm{Render}} + \mathcal{L}_{\mathrm{KL}} + \mathcal{L}_{\mathrm{Score}} + \mathcal{L}_{\mathrm{Geo}} $$
其中 $\mathcal{L}_{\mathrm{Render}} = \mathcal{L}_1(I, I_{GT}) + \lambda_{\mathrm{D-SSIM}} \cdot (1 - \mathrm{SSIM}(I, I_{GT}))$ 保证像素与结构保真度，$\mathcal{L}_{\mathrm{KL}}$ 和 $\mathcal{L}_{\mathrm{Score}}$ 分别对应情绪分布的 KL 蒸馏和情绪强度的 L1 回归，$\mathcal{L}_{\mathrm{Geo}}$ 为几何正则项。

![[assets/figures/papers/paper_list_l2475_https_arxiv_org_abs_2603_21332/figures/003_Figure_3.jpg]]
*Figure 3: Overview of EmoTaG. For pretraining, our Gated Residual Motion Network learns a universal motion prior from a multi-identity corpus. This network comprises an Identity-Conditioned Encoder for integrating audio, expression, and identity through AdaIN-based modulation, followed by an Expert Motion Decoder that leverages emotion-distilled supervision to train three cooperative branches (Base, Residual, Gate). During adaptation, the Gated Residual Motion Network is efficiently adapted to a new identity from 5-second video via only tuning the AdaIN modulation parameters. At inference, the adapted model produces expressive, high-fidelity 3D facial animation driven by new audio with head pose and...*

EmoTaG 的整体架构围绕两个核心组件展开：**FLAME-Gaussian 模型**提供结构化 3D 先验，**门控残差运动网络 (GRMN)** 负责从多模态驱动信号中预测动态面部运动。以下逐一拆解关键模块及其数学形式。

### FLAME-Gaussian 模型：结构化 3D 先验

FLAME 是一种参数化面部模型，其输出网格由形状参数 $\beta$、表情参数 $\Psi$ 和姿态参数 $\Theta$ 控制：

$$M(\beta,\Psi,\Theta) \in \mathbb{R}^{3 \times N}$$

EmoTaG 将场景表示为 $K$ 个各向异性 3D 高斯，每个高斯 $g_i$ 包含中心 $\pmb{\mu}_i$、旋转 $\pmb{r}_i$、尺度 $\pmb{s}_i$、透明度 $\alpha_i$ 和球谐系数 $\mathbf{SH}_i$：

$$\mathcal{G} = \{g_i\}_{i=1}^K, \quad g_i = (\pmb{\mu}_i, \pmb{r}_i, \pmb{s}_i, \alpha_i, \mathbf{SH}_i)$$

高斯中心通过重心坐标在 FLAME 网格三角形内插值初始化：

$$\pmb{\mu}_i = \sum_{j=1}^3 w_{ij} \mathbf{v}_j, \quad \sum w_{ij}=1$$

在动画驱动时，每个高斯通过其父三角形的旋转 $\mathbf{R}^j$、中心 $\mathbf{C}^j$ 和缩放因子 $k^j$ 从局部坐标变换到全局空间：

$$\mathcal{G}_i = \left\{ \begin{array}{ll} \pmb{\mu}_i = k^j \mathbf{R}^j \pmb{\mu}_l + \mathbf{C}^j, \\ \pmb{r}_i = \mathbf{R}^j \pmb{r}_l, \\ \pmb{s}_i = k^j \pmb{s}_l, \\ \alpha_i = \alpha_l, \\ \mathbf{SH}_i = \mathbf{SH}_l \end{array} \right.$$

这一设计将运动预测从直接变形 3D 高斯重新形式化为 FLAME 参数回归，利用 FLAME 网格的强结构化先验确保运动几何稳定性。

### 门控残差运动网络 (GRMN)

GRMN 由**身份条件编码器**和**专家运动解码器**两部分组成，负责融合音频、表情和身份信息，输出 FLAME 表情参数和下巴姿态参数。

#### 身份条件编码器

身份条件编码器通过 AdaIN 调制将身份特征 $\mathbf{s}$ 注入音频和表情特征。身份特征经 MLP 预测缩放因子 $\gamma$ 和偏置 $\beta$：

$$\gamma, \beta = \mathrm{MLP}(\mathbf{s})$$

随后对目标特征 $\mathbf{F}$ 进行自适应实例归一化：

$$\tilde{\mathbf{F}} = \gamma \cdot \mathrm{InstanceNorm}(\mathbf{F}) + \beta$$

这种调制机制使网络能够学习个性化的运动风格，是少样本个性化适应的关键。

#### 专家运动解码器

解码器包含三个协作分支：

- **基分支 (Base Branch)**：捕捉与语音内容相关的中性运动模式。
- **残差分支 (Residual Branch)**：建模情绪相关的运动偏差。
- **门控分支 (Gate Branch)**：自适应融合基分支与残差分支的输出。

最终运动 $\delta$ 由基分支输出 $\delta_{\mathrm{b}}$ 与门控加权后的残差 $\delta_{\mathrm{r}}$ 组合而成：

$$\delta = \delta_{\mathrm{b}} + g \cdot \delta_{\mathrm{r}}$$

其中 $g$ 为门控分支输出的融合权重。这种解耦设计使网络能够在中性语音运动与情绪调制之间实现自适应平衡。

### 口内细化模块

对于位于口内区域的高斯子集 $\mathcal{G}_{\mathrm{mouth}}$，网络额外预测残差偏移以增强精细口腔动画细节：

$$\pmb{\mu}^* = \pmb{\mu} + \Delta \pmb{\mu}, \quad \pmb{r}^* = \pmb{r} + \Delta \pmb{r}, \quad \pmb{s}^* = \pmb{s} + \Delta \pmb{s}$$

该模块仅作用于口内高斯的位置、旋转和尺度，在不增加全局计算负担的前提下提升唇部细节表现力。

### 语义情绪引导 (SEG)

SEG 采用教师-学生蒸馏框架，以预训练情绪识别器 DeepFace 作为教师模型。教师提供两个监督信号：

- **情绪分布**：类别级情绪概率分布，用于 KL 蒸馏。
- **情绪强度分数**：标量情绪强度，定义为非中性情绪的概率之和：

$$e = 1 - p_{\mathrm{emo}}(\mathrm{neutral})$$

这两个信号分别指导残差分支和门控分支的学习，使 GRMN 无需人工情绪标注即可获得情绪感知能力。

### 训练目标

完整训练损失由四项组成：

$$\mathcal{L} = \mathcal{L}_{\mathrm{Render}} + \mathcal{L}_{\mathrm{KL}} + \mathcal{L}_{\mathrm{Score}} + \mathcal{L}_{\mathrm{Geo}}$$

其中渲染损失组合 L1 损失和 D-SSIM 损失以保持像素与结构保真度：

$$\mathcal{L}_{\mathrm{Render}} = \mathcal{L}_1(I, I_{GT}) + \lambda_{\mathrm{D\text{-}SSIM}} \cdot (1 - \mathrm{SSIM}(I, I_{GT}))$$

$\mathcal{L}_{\mathrm{KL}}$ 为情绪分布的 KL 蒸馏损失，$\mathcal{L}_{\mathrm{Score}}$ 为情绪强度的 L1 回归损失，$\mathcal{L}_{\mathrm{Geo}}$ 为几何正则化项。

## 实验与关键发现

### 动机验证：情绪音频的运动复杂性

情绪驱动说话人脸的核心挑战在于情绪音频引发的唇部运动远比中性音频复杂。EmoTaG通过分析唇部关键点的水平与垂直张开轨迹，量化了这一差异（Figure 2）：情绪音频下嘴部运动的标准差达到 **7.88** 和 **6.92**，而中性音频仅为 **3.11**。这种强烈的时序波动意味着，直接变形3D高斯的方法在情绪场景下极易产生几何不稳定和音频-运动失配，从而奠定了引入显式几何先验与情绪解耦建模的必要性。

### 自重建主实验

Table 1 报告了在5秒训练数据设定下，中性与情绪视频的自重建定量对比。EmoTaG在所有评估维度上均取得最优结果：

![[assets/figures/papers/paper_list_l2475_https_arxiv_org_abs_2603_21332/figures/006_Table_1.jpg]]
*Table 1: Quantitative comparison on self-reconstruction of neutral and emotional talking videos with 5s training data. and indicate the 1st and 2nd best results on the neutral set, while and indicate the 1st and 2nd best results on the emotional set. Efficiency columns (Train, FPS) are ranked using the red palette*

- **中性场景**：PSNR **30.02**，LPIPS **0.019**，SSIM **0.883**，LMD **2.221**，Sync-C **6.212**。
- **情绪场景**：PSNR **29.95**，LPIPS **0.022**，SSIM **0.877**，LMD **2.456**，Sync-C **6.147**。

与次优基线（如 **InsTaG**（Li et al., CVPR 2025）和 **MimicTalk**（Ye et al., NeurIPS 2024））相比，EmoTaG在情绪集上的LMD（地标运动距离）和AUE（上下脸动作单元误差）优势尤为突出，表明FLAME参数回归策略有效约束了情绪驱动的面部形变，避免了直接预测高斯变形带来的运动抖动。定性结果（Figure 5）进一步显示，基线方法在情绪表达时出现口部扭曲和上脸运动不自然的问题，而EmoTaG保持了时序连贯的唇形与自然的上脸动态。

![[assets/figures/papers/paper_list_l2475_https_arxiv_org_abs_2603_21332/figures/005_Figure_5.jpg]]
*Figure 5: Qualitative comparison on self-reconstruction. EmoTaG generates more expressive, temporally coherent, and wellsynchronized talking heads than previous methods across both neutral and emotional test cases. It preserves accurate mouth articulation and natural upper-face motion even under challenging expressions. The red rectangles highlight regions where previous methods produce distorted and inaccurate facial motions. We strongly recommend watching the supplementary video for dynamic comparison*

### 情绪强度泛化

为检验模型对未知情绪强度的适应能力，实验在中等强度（Level-2）数据上微调，在弱情绪（Level-1）和强情绪（Level-3）上测试（Table 2）。EmoTaG在两个泛化层级上均保持领先：Level-1下Sync-C达 **6.154**，Level-3下Sync-C为 **6.126**，且LMD和AUE指标均低于所有基线。这验证了语义情绪引导（SEG）蒸馏的情绪分布知识使GRMN的残差分支学会了连续的情绪强度表征，而非简单过拟合训练强度。

![[assets/figures/papers/paper_list_l2475_https_arxiv_org_abs_2603_21332/figures/007_Table_2.jpg]]
*Table 2: Quantitative comparison on emotion-intensity. We adapt models on Level-2 (medium) and test on Level-1 (weaker) and Level-3 (stronger) separately. [Key: Best, Second Best]*

### 跨身份与跨语言泛化

Table 3 评估了分布外（OOD）音频驱动的唇音同步性能，涵盖跨身份和跨语言两种挑战场景。EmoTaG在Sync-C指标上均排名第一，证明身份条件编码器中的AdaIN调制成功将个性化运动风格与通用语音-运动映射解耦，使得模型在未见说话人或语言时仍能保持准确的唇音对齐。

![[assets/figures/papers/paper_list_l2475_https_arxiv_org_abs_2603_21332/figures/008_Table_3.jpg]]
*Table 3: Quantitative results of lip synchronization on OOD audio-driven. We evaluate two challenging scenarios: crossidentity and cross-language. [Key: Best, Second Best]*

### 用户主观研究

20名参与者的Likert 1-5评分（Table 4）从情绪表现力、唇同步和视觉真实感三个维度进行主观评价。EmoTaG在所有维度上均获最高分，与客观指标趋势一致，特别在情绪表现力上显著优于缺乏显式情绪建模的基线方法。

### 消融实验

Table 5 在情绪测试集上系统消融了EmoTaG的关键组件：

![[assets/figures/papers/paper_list_l2475_https_arxiv_org_abs_2603_21332/figures/010_Table_5.jpg]]
*Table 5: Ablation study of EmoTaG. Evaluated under the 5s selfreconstruction setting on the emotional test set, showing the effect of each component on quality and synchronization*

| 移除组件 | PSNR | LMD | Sync-C | 核心影响 |
|---------|------|-----|--------|---------|
| 完整模型 | 29.95 | 2.456 | 6.147 | — |
| 语义情绪引导 (SEG) | 29.01 | 3.067 | 5.541 | 情绪表达与同步全面退化 |
| 分数蒸馏损失 (L_Score) | — | 显著上升 | — | 主要损害音频-运动同步 |
| KL蒸馏损失 (L_KL) | — | — | — | 运动精度与视觉保真度下降 |
| 门控分支 | — | — | — | 引入时序不稳定，削弱同步 |
| AdaIN身份调制 | **28.38** | **4.021** | **4.621** | 性能降幅最大，个性化建模核心 |

**关键发现**：
1. **AdaIN身份调制**的移除造成最严重的性能崩塌（PSNR下降1.57，LMD上升1.565），证实个性化运动风格建模是少样本适应的瓶颈组件。
2. **语义情绪引导（SEG）**的移除导致LMD从2.456升至3.067，Sync-C从6.147降至5.541，说明情绪蒸馏对运动精度和情绪-音频一致性的关键作用。Figure 6的定性对比进一步显示，无SEG时上脸表情显著减弱，情绪-音频失配明显。
3. **门控分支**的消融揭示了基分支与残差分支简单相加无法自适应调节情绪相关运动的贡献强度，导致时序不稳定。

### 效率分析

Table 1的效率列显示，EmoTaG在单块NVIDIA RTX A6000 GPU上的训练时间与推理FPS均具有竞争力。得益于仅微调AdaIN参数的轻量适应策略，新身份个性化仅需20K迭代，显著降低了少样本场景的计算开销。

## 定位与知识库关联

### 1. 方法谱系：从3D高斯说话人到情绪感知生成

EmoTaG 建立在少样本3D说话人头像合成的技术脉络上，其直接前身是 **InsTaG**（Li et al., CVPR 2025）。InsTaG 首次将 3D Gaussian Splatting 引入少样本说话人合成，通过直接预测高斯变形参数来驱动面部运动。然而，这种无约束的变形预测在面对情绪语音时暴露出几何不稳定和音频-情绪不匹配的问题——Figure 2 揭示，情绪音频的嘴部运动轨迹标准差高达 7.88，远高于中性音频的 3.11，说明情绪驱动的面部运动复杂度显著增加，直接变形策略难以胜任。

EmoTaG 的核心突破在于**将运动预测重新形式化为 FLAME 参数回归**。这一设计选择并非偶然：FLAME 作为成熟的3D可变形人脸模型，提供了强结构化先验（shape、expression、jaw pose 参数空间），使得运动预测从自由变形退化为低维参数空间的回归问题，从而天然保证了运动几何的一致性。这一思路与 **MimicTalk**（Ye et al., NeurIPS 2024）和 **Real3D-Portrait**（Ye et al., arXiv 2024）等同期工作形成对比：后两者虽也追求表达性3D说话人，但未显式引入情绪建模机制。

在运动生成架构上，EmoTaG 的 **Gated Residual Motion Network (GRMN)** 借鉴了 Mixture-of-Experts 的思想，将运动解耦为基分支（捕捉语音中性运动）和残差分支（建模情绪相关偏差），通过门控分支实现自适应融合。这种解耦设计在说话人合成领域尚属首次，其灵感可能来自语音转换和情感语音合成中的解耦范式，但 EmoTaG 将其迁移到3D几何空间，并通过 AdaIN 身份调制注入个性化运动风格。

情绪建模方面，EmoTaG 的 **Semantic Emotion Guidance (SEG)** 采用教师-学生蒸馏框架，以预训练情绪识别器 DeepFace 为教师，无需人工情绪标注即可学习情绪分布和强度。这一弱监督策略显著降低了数据获取成本，与 **GeneFace++**（Ye et al., arXiv 2023）等依赖显式情绪标签的方法形成差异化优势。

### 2. 知识库定位：关键设计选择与因果机制

EmoTaG 对知识库的贡献可归纳为三个层次：

**层次一：运动表示的重构。** 将“直接预测3D高斯变形”替换为“预测FLAME参数→FLAME网格驱动→高斯绑定变换”，这一变化槽位（changed slot）的因果效应是：运动稳定性从无约束变形空间转移到有界参数空间，消融实验虽未直接量化该槽位的独立贡献，但移除 FLAME-Gaussian 映射将导致方法退化为 InsTaG 的变形预测范式，其在情绪场景下的性能劣化可由 InsTaG 与 EmoTaG 的对比间接推断（Table 1 中 EmoTaG 在情绪集上全面领先）。

**层次二：运动生成的解耦与融合。** GRMN 的三分支设计（基/残差/门控）是 EmoTaG 最核心的架构创新。消融实验（Table 5）提供了直接的因果证据：移除门控分支导致时间不稳定性增加和音频-运动同步下降，证实了自适应融合机制的必要性。移除 AdaIN 身份调制造成 PSNR 从 29.95 骤降至 28.38，LMD 从 2.456 升至 4.021，Sync-C 从 6.147 降至 4.621——这是所有消融项中性能降幅最大的，揭示了**个性化运动风格建模是少样本场景的核心瓶颈**，而 AdaIN 调制是解决该瓶颈的关键设计。

**层次三：情绪知识的蒸馏注入。** SEG 模块通过两个损失函数实现情绪蒸馏：KL 蒸馏损失（$\mathcal{L}_{\mathrm{KL}}$）传递情绪分布知识，分数回归损失（$\mathcal{L}_{\mathrm{Score}}$）传递情绪强度知识。消融实验表明，移除 SEG 导致 PSNR 从 29.95 降至 29.01，LMD 从 2.456 升至 3.067，Sync-C 从 6.147 降至 5.541。值得注意的是，移除 $\mathcal{L}_{\mathrm{Score}}$ 主要损害音频-运动同步（LMD 明显上升），而移除 $\mathcal{L}_{\mathrm{KL}}$ 导致运动精度和视觉保真度显著下降——这暗示**情绪分布知识主要服务于运动精度，情绪强度知识主要服务于时序对齐**，两者在功能上存在分工。

### 3. 适用边界与局限

**适用场景：** EmoTaG 在少样本（5秒训练数据）个性化场景下表现最优，覆盖中性语音和情绪语音的自重建任务，并展现出对情绪强度（弱/强）和跨语言/跨身份驱动的泛化能力（Table 2, Table 3）。其训练效率（单块 NVIDIA RTX A6000 GPU）和推理 FPS 在 Table 1 中排名前列，具备实用部署潜力。

**已知局限：** 论文未明确列出局限性章节，但从方法设计可推断以下边界：

- **情绪类别依赖教师模型。** SEG 的情绪分布质量受限于 DeepFace 的识别能力，对于 DeepFace 未覆盖的情绪类别或文化特定的表情模式，蒸馏效果可能下降。这一局限在论文中未被消融验证，需手动确认。
- **FLAME 先验的表达力上限。** FLAME 作为线性模型，对极端表情（如夸张的恐惧或厌恶）的建模能力有限，可能导致口内残差预测（Eq. 8）承担过多补偿，在极端情绪下出现伪影。
- **身份泛化的隐性假设。** AdaIN 调制假设身份风格可通过缩放和偏置参数线性注入，对于运动风格与训练集分布差异极大的新身份，该假设可能不成立。用户研究（Table 4）虽显示 EmoTaG 在情绪表达和视觉真实感上优于基线，但未报告失败案例。

**开放问题：** 论文未明确列出开放问题，但从技术路线可识别以下待探索方向：

- **多模态情绪控制。** 当前 SEG 仅从音频蒸馏情绪，未利用文本或视频中的情绪线索，多模态融合可能进一步提升情绪感知精度。
- **长期时序一致性。** 实验仅在短片段上评估，长时间生成中的情绪漂移和几何累积误差未被讨论。
- **与扩散模型的结合。** 近期扩散模型在2D说话人合成中展现出强表达力，EmoTaG 的 FLAME 参数预测框架是否可与扩散先验结合，是值得探索的方向。

## 原文 PDF

![[paperPDFs/CVPR_2026/EmoTaG_Emotion_Aware_Talking_Head_Synthesis_on_Gaussian_Splatting_with_Few_Shot_Personalization.pdf]]

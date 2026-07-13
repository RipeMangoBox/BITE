---
title: "InfinityHuman: Towards Long-Term Audio-Driven Human Animation"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/InfinityHuman_Towards_Long_Term_Audio_Driven_Human_Animation.pdf
project_link: "https://infinityhuman.github.io/"
code_link: "https://github.com/ultralytics/"
aliases:
- InfinityHuman
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 将姿态序列解耦视觉表现作为稳定几何控制信号，并结合参考图作为视觉锚点，以及引入手部特定奖励反馈机制。
primary_logic: 姿态序列结构上不受外观退化影响，可以作为长期生成中保持身份一致性和动作连贯性的无漂移引导；同时利用参考帧建立身份锚点，并通过手部奖励机制纠正细小关节失真。
claims:
- InfinityHuman 在 EMTD 和 HDTF 数据集上的视频质量、身份保持、手部精度和唇形同步达到 SOTA 性能。
- 去除姿态引导细化器导致 FID 从 91.74 增加到 109.54，FSIM 从 0.88 下降到 0.79。
- 去除手部奖励反馈导致手部关键点精度 HKC 从 0.87 下降至 0.85。
- 长时间视频稳定性评估显示，随着时长增加，FID、FVD、FSIM 和 Sync 指标保持稳定。
---

# InfinityHuman: Towards Long-Term Audio-Driven Human Animation

> [!tip] 核心洞察
> 姿态序列结构上不受外观退化影响，可以作为长期生成中保持身份一致性和动作连贯性的无漂移引导；同时利用参考帧建立身份锚点，并通过手部奖励机制纠正细小关节失真。

| 字段 | 内容 |
|------|------|
| 中文题名 | InfinityHuman：面向长时间音频驱动人体动画 |
| 英文题名 | InfinityHuman: Towards Long-Term Audio-Driven Human Animation |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Li_InfinityHuman_Towards_Long-Term_Audio-Driven_Human_Animation_CVPR_2026_paper.html) · [Project](https://infinityhuman.github.io/) · [Code](https://github.com/ultralytics/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | InfinityHuman |
| Dataset | EMTD, HDTF |

> [!tip] 效果简介
> - EMTD 上，FID↓ 69.28；FVD↓ 239.05；IQA↑ 2.11。
> - HDTF 上，FID↓ 60.71；FVD↓ 979.88；IQA↑ 2.48。

## 概要

**研究问题**：长时音频驱动人体动画面临两大核心瓶颈。其一，长视频生成中的误差累积导致人物身份漂移、颜色偏移和场景不稳定（Figure 2）；其二，手部运动建模缺失，造成手势失真以及与音频信号的不对齐。现有方法如 **HunyuanVideo-Avatar**（Chen et al., arXiv 2025）、**OmniHuman-1**（Lin et al., ICCV 2025）等在长时间序列上普遍出现面部一致性退化、背景闪烁和手部伪影。

**核心思路**：InfinityHuman 提出一种**由粗到细的两阶段生成框架**（Figure 3）。第一阶段（LR-A2V）从音频和参考图生成低分辨率运动视频；第二阶段（Pose-Guided Refiner）利用**解耦的姿态序列作为稳定几何控制信号**，配合参考帧作为视觉锚点，将低分辨率视频恢复为高分辨率输出。姿态序列在结构上不受外观退化影响，因此可作为长期生成中保持身份一致性和动作连贯性的无漂移引导。此外，引入**手部特定奖励反馈机制**（Hand-Specific Reward Feedback Learning），通过预训练的手部质量奖励模型纠正细小关节失真。

**主要结果**：在 EMTD 和 HDTF 数据集上，InfinityHuman 在视频质量（FID、FVD）、身份保持（FaceSIM）、手部精度（HKC）和唇形同步（Sync）等指标上达到 SOTA 性能（Table 1）。长视频稳定性评估显示，从 10s 到 50s 的累计指标保持稳定，无明显退化（Table 3）。

**方法定位**：InfinityHuman 属于两阶段音频驱动全身动画方法，区别于单阶段直接生成的基线。其关键创新在于将姿态序列与外观表现解耦作为长期控制信号，并首次在音频驱动人体动画中引入手部专项优化。当前框架仅训练于单人连续视频，对多人交互和场景切换的支持仍需扩展。



音频驱动的人体动画旨在从语音信号中合成逼真的说话人物视频，在虚拟主播、数字人交互、电影制作等领域具有广泛应用。然而，现有方法在生成**长时间视频**时面临根本性瓶颈：随着生成时长增加，累积误差导致人物身份漂移、颜色偏移、场景不稳定等视觉退化现象（Figure 2）。这一问题的根源在于，先前工作通常将前一时刻的生成帧作为下一时刻的条件输入，误差沿时间轴逐步放大，形成“滚雪球”效应。

与此同时，**手部运动建模**是另一长期被忽视的挑战。由于手部关节自由度极高、训练数据中手部区域占比较小，现有方法生成的视频频繁出现手指畸变、手势与音频节奏不对齐等问题。此前的工作如 **HunyuanVideo-Avatar**（Chen et al., arXiv 2025）、**OmniAvatar**（Gan et al., arXiv 2025）、**OmniHuman-1**（Lin et al., ICCV 2025）等虽在全身体动画上取得进展，但均未专门优化手部生成质量；而 **Hallo3**（Cui et al., CVPR 2025）、**FantasyTalking**（Wang et al., ACM Multimedia 2025）等方法仅聚焦于头部动画，无法处理全身动作。

上述两大缺口——**长时视觉一致性**与**手部运动保真度**——构成了本文的核心动机。InfinityHuman 的出发点是：若能引入一种结构上不受外观退化影响的控制信号来引导生成，并辅以手部特定的反馈机制，就有望同时解决身份漂移与手势失真问题。具体而言，姿态序列（pose sequence）作为纯几何信息，天然不受颜色、纹理等外观退化影响，可作为长时生成中的**无漂移引导**；同时，参考帧可作为身份锚点，锁定人物外观；而手部奖励反馈则可针对性地纠正细小关节畸变。基于这些洞察，本文提出由粗到细的两阶段框架 InfinityHuman，系统性地应对长时间音频驱动人体动画中的核心挑战。



## 核心方法与创新机理

InfinityHuman 的核心创新并非单一模块的修补，而是针对长时音频驱动人体动画中**误差累积**与**精细部位失真**两大瓶颈，提出了一套**由粗到细的解耦生成范式**。其关键创新点可归纳为以下四个维度的 changed slots：

### 1. 两阶段解耦生成范式：从直接生成到“粗粒度运动基元 + 细粒度视觉修复”

现有方法（如 **HunyuanVideo-Avatar** (Chen et al., arXiv 2025)、**OmniHuman-1** (Lin et al., ICCV 2025) 等）普遍采用单阶段直接生成高分辨率视频的策略。这种端到端方式在长时生成中面临严重的误差累积——早期帧的微小瑕疵会作为条件输入后续帧，导致身份漂移、颜色偏移和场景不稳定（见 Figure 2）。

InfinityHuman 将这一过程解耦为两个级联阶段：
- **LR-A2V（低分辨率音频到视频生成）**：首先在低分辨率空间生成与音频同步的粗粒度运动视频。低分辨率潜空间天然具有更强的语义鲁棒性，能够以较低计算代价建立稳定的时序运动基元。
- **PG-Refiner（姿态引导细化器）**：随后利用解耦的姿态序列作为无漂移的几何控制信号，将低分辨率视频恢复为高分辨率输出。

这一设计的深层洞察在于：**姿态序列在结构上不受外观退化影响**，可以作为长期生成中保持动作连贯性的稳定锚点。消融实验证实了该范式的关键作用——去除 PG-Refiner 后，FID 从 91.74 急剧上升至 109.54，FSIM 从 0.88 下降至 0.79（Table 2）。

### 2. 时序条件信号重构：从“运动帧条件”到“姿态锚点 + 参考帧锚点”

传统方法将先前生成的视频帧直接作为时序条件，这导致外观误差沿时间轴传播。InfinityHuman 重构了条件信号体系：

- **姿态序列作为几何控制信号**：从 LR-A2V 输出中提取的姿态关键点序列，仅编码人体几何结构信息，天然隔离了纹理、光照等外观退化因素。
- **前缀潜在参考策略（Prefix-Latent Reference）**：将参考帧作为视觉身份锚点注入细化器，而非依赖结构对齐参考网络。具体而言，高分辨率噪声注入策略（Eq. 6）仅对未来帧添加噪声，保持前 $m$ 帧为干净参考，同时通过损失掩码（Eq. 8）排除前缀帧的损失计算，确保身份一致性不被训练目标干扰。
- **退化低分辨率潜变量条件**：对 LR 潜变量进行低通滤波并添加高斯噪声（Eq. 5: $z^{\mathrm{deglr}} = \mathrm{LPF}(z^{\mathrm{lr}}) + \alpha_{\mathrm{deg}} \cdot \epsilon$），模拟真实生成场景中的时序退化，增强细化器的鲁棒性。

消融实验表明，去除低分辨率视频潜在条件或姿态引导条件均导致显著的生成质量下降（Table 2），验证了双重锚点设计的必要性。

### 3. 手部特定奖励反馈学习：从“无专门手部优化”到“奖励驱动的精细关节校正”

现有音频驱动动画方法普遍缺乏对手部运动的专门建模，导致手势失真、手指畸变、与音频节奏不对齐等问题。InfinityHuman 引入了**手部特定奖励反馈学习**机制：

- 预训练一个手部质量奖励模型 $r_{\mathrm{hand}}$，对随机采样的解码帧进行手部关键点精度评估。
- 通过奖励损失（Eq. 9: $\mathcal{L}_{\mathrm{hand}}(\theta) = \mathbb{E}_{c \sim p(c)} \mathbb{E}_{X_i^{\mathrm{lr}} \sim \mathcal{D}(z_{i,1}^{\mathrm{lr}})} [T - r_{\mathrm{hand}}(X_i^{\mathrm{lr}}, c)]$）直接优化生成模型，使其在奖励信号的引导下减少手部畸变。
- 配合高质量手部数据的针对性训练，形成“数据 + 奖励”双重校正策略。

定量结果表明，去除手部奖励反馈后，手部关键点精度 HKC 从 0.87 下降至 0.85（Table 2）。虽然绝对降幅看似有限，但在长时生成场景下，这一机制有效抑制了手部畸变的累积放大效应。

### 4. 多模态条件解耦注入：从“融合交叉注意力”到“独立音频分支”

传统方法通常将文本和音频条件融合后通过统一的交叉注意力注入生成网络。InfinityHuman 采用**解耦的多模态交叉注意力**（Eq. 4）：

$$\mathrm{CA}_{\mathrm{mm}}(x^{\mathrm{lr}}, c_{\mathrm{text}}, c_{\mathrm{audio}}) = \mathrm{CA}(x^{\mathrm{lr}}, c_{\mathrm{text}}) + \mathrm{CA}(x^{\mathrm{lr}}, c_{\mathrm{audio}})$$

文本和音频条件通过独立的交叉注意力分支注入，避免了模态间的信息干扰。配合训练时的多重条件 Dropout 策略（文本和音频各以 10% 概率独立丢弃，参考图和首帧以 10% 概率丢弃），增强了模型对各条件信号的解耦感知能力，从而提升音画对齐精度和身份保持鲁棒性。



InfinityHuman 提出了一种**由粗到细的两阶段生成框架**，专门解决长时间音频驱动人体动画中的视觉退化与身份漂移问题。其核心设计思路是：先以低分辨率生成与音频同步的粗粒度运动视频，再通过姿态引导的细化器将其恢复为高分辨率、身份一致的长时间输出。

### 两阶段流水线

流水线由两个核心模块串联构成（Figure 3）：

![[assets/figures/papers/paper_list_l1066_https_openaccess_thecvf_com_content_CVPR2026_html_Li_InfinityHuman_Towar/figures/003_Figure_3.jpg]]
*Figure 3: InfinityHuman Pipeline. The pipeline generates high-resolution (HR) audio-driven full-body videos through a two-stage coarseto-fine process. First, a speech-aligned low-resolution (LR) video is generated using multimodal conditioning (text and audio) and DiT blocks. In the second stage, a pose-guided refiner utilizes pose guidance, LR latents, and reference images to restore degraded details, enhancing identity consistency, motion coherence, and hand realism*

1. **低分辨率音频到视频生成（LR-A2V, §3.1）**  
   输入为参考图像 $I_{\mathrm{ref}}$、文本描述 $c_{\mathrm{text}}$ 和音频特征 $c_{\mathrm{audio}}$，输出一段低分辨率运动视频潜变量序列 $\{z_i^{\mathrm{lr}}\}_{i=0}^f$。该阶段采用基于流匹配的 DiT 架构，通过**解耦的多模态交叉注意力**（Eq.4）独立注入文本与音频条件：
   $$\mathrm{CA}_{\mathrm{mm}}(x^{\mathrm{lr}}, c_{\mathrm{text}}, c_{\mathrm{audio}}) = \mathrm{CA}(x^{\mathrm{lr}}, c_{\mathrm{text}}) + \mathrm{CA}(x^{\mathrm{lr}}, c_{\mathrm{audio}})$$
   这种设计使音频驱动的唇形与肢体运动与文本语义控制互不干扰。

2. **姿态引导细化器（PG-Refiner, §3.2）**  
   将 LR-A2V 输出的低分辨率视频恢复为高分辨率。关键创新在于引入两类“无漂移”锚定信号：
   - **姿态序列 $P'$**：从 LR 视频中提取的骨架姿态，结构上不受外观退化影响，作为稳定的几何控制信号；
   - **前缀潜在参考（prefix-latent reference）**：将参考帧的潜变量作为视觉身份锚点，约束生成过程中的人物外观一致性。

   细化器对退化后的低分辨率潜变量 $z^{\mathrm{deglr}}$（经低通滤波与噪声增强，Eq.5）进行条件化，并采用**仅对未来帧注入噪声**的策略（Eq.6），保持前 $m$ 帧为干净参考以提供身份与运动引导。损失函数通过掩码 $w_i$（Eq.8）仅计算未来帧的速度预测误差（Eq.7），避免对锚定帧的干扰。

### 手部特定奖励反馈学习

作为流水线的补充优化环节（§3.3），InfinityHuman 引入**手部特定奖励反馈学习**：利用预训练的手部质量奖励模型 $r_{\mathrm{hand}}$，对随机采样的解码帧计算奖励差异，并以此作为优化目标（Eq.9）：
$$\mathcal{L}_{\mathrm{hand}}(\theta) = \mathbb{E}_{c \sim p(c)} \mathbb{E}_{X_i^{\mathrm{lr}} \sim \mathcal{D}(z_{i,1}^{\mathrm{lr}})} \left[ T - r_{\mathrm{hand}}(X_i^{\mathrm{lr}}, c) \right]$$
该机制显式纠正手指关节畸变，弥补现有方法在手部建模上的缺失。

### 模块间数据流关系

整体数据流可概括为：
```
参考图像 + 文本 + 音频
        ↓
    LR-A2V（DiT + 解耦交叉注意力）
        ↓
  低分辨率视频潜变量 z^lr
        ↓
   姿态提取 + 退化增强 → z^deglr
        ↓
   PG-Refiner（姿态引导 + 前缀参考）
        ↓
  高分辨率视频 + 手部奖励反馈优化
        ↓
      最终输出
```

### 关键设计决策

| 设计槽位 | 基线做法 | InfinityHuman 做法 | 依据 |
|---------|---------|-------------------|------|
| 整体框架 | 单阶段直接生成 | 两阶段由粗到细（LR-A2V + PG-Refiner） | §3, §3.1, §3.2 |
| 时序条件信号 | 使用先前运动帧作为条件 | 使用解耦的姿态序列和参考帧作为锚点 | §3.2 |
| 手部建模 | 无专门手部优化 | 手部特定奖励反馈学习 | §3.3 |
| 音频条件注入 | 融合交叉注意力 | 解耦的多模态交叉注意力（独立音频分支） | §3.1, Eq.(4) |
| 参考帧处理 | 结构对齐参考网络 | 前缀潜在参考策略 | §3.2 |

这一框架的核心洞察在于：**姿态序列结构上不受外观退化影响，可作为长期生成中保持身份一致性和动作连贯性的无漂移引导**；同时利用参考帧建立身份锚点，并通过手部奖励机制纠正细小关节失真。



InfinityHuman 采用两阶段由粗到细的生成框架，其核心由四个关键模块构成：低分辨率音频到视频生成器（LR-A2V）、姿态引导细化器（PG-Refiner）、手部特定奖励反馈学习机制，以及多模态条件交叉注意力。以下逐一阐述各模块的设计逻辑与关键公式。

### 3.1 低分辨率音频到视频生成（LR-A2V）

第一阶段的目标是从音频和参考图像生成时序对齐的低分辨率运动视频。该模块基于流匹配（flow matching）框架，在潜在空间中建模视频帧的生成过程。

对于第 $i$ 帧的低分辨率潜在表示 $z_i^{\mathrm{lr}}$，其在扩散时间 $t$ 的噪声化版本通过线性插值得到：

$$z_{i,t}^{\mathrm{lr}} = \phi(z_i^{\mathrm{lr}}, t) = (1 - t) \cdot \epsilon_i + t \cdot z_{i,1}^{\mathrm{lr}} \tag{1}$$

其中 $\epsilon_i \sim \mathcal{N}(0, I)$ 为标准高斯噪声，$z_{i,1}^{\mathrm{lr}}$ 为干净的潜在帧。对应的目标速度场定义为干净潜在与噪声之差：

$$v_{i,t} = \frac{d z_{i,t}^{\mathrm{lr}}}{d t} = z_{i,1}^{\mathrm{lr}} - \epsilon_i \tag{2}$$

DiT 模型 $f_\theta$ 以噪声化潜在序列、参考图像 $I_{\mathrm{ref}}$、文本条件 $c_{\mathrm{text}}$ 和音频条件 $c_{\mathrm{audio}}$ 为输入，预测速度场。训练目标为最小化预测速度与真实速度的均方误差：

$$\mathcal{L} = \mathbb{E}_{\epsilon_i \sim \mathcal{N}(0, I), t \sim \mathcal{U}(0,1)} \left\| f_{\theta} \left( \{ z_{i,t}^{\mathrm{lr}} \}_{i=0}^{f}, I_{\mathrm{ref}}, c_{\mathrm{text}}, c_{\mathrm{audio}}, t \right) - \{ v_{i,t} \}_{i=0}^{f} \right\|_2^2 \tag{3}$$

**多模态条件注入**：为增强音频与视觉的对齐，该模块采用解耦的多模态交叉注意力机制，将文本和音频条件分别通过独立的交叉注意力分支注入：

$$\mathrm{CA}_{\mathrm{mm}} \bigl( x^{\mathrm{lr}}, c_{\mathrm{text}}, c_{\mathrm{audio}} \bigr) = \mathrm{CA} \bigl( x^{\mathrm{lr}}, c_{\mathrm{text}} \bigr) + \mathrm{CA} \bigl( x^{\mathrm{lr}}, c_{\mathrm{audio}} \bigr) \tag{4}$$

这种设计避免了文本和音频特征在单一注意力分支中的相互干扰，使模型能更精确地捕捉音频-嘴型对应关系。

### 3.2 姿态引导细化器（PG-Refiner）

第二阶段的核心挑战在于：低分辨率视频在长时序生成中会累积误差，导致身份漂移和场景不稳定。PG-Refiner 通过两个关键设计解决此问题。

**退化低分辨率潜在表示**：首先对第一阶段输出的低分辨率潜在 $z^{\mathrm{lr}}$ 施加低通滤波并添加高斯噪声，模拟长视频中的时序退化：

$$z^{\mathrm{deglr}} = \mathrm{LPF}(z^{\mathrm{lr}}) + \alpha_{\mathrm{deg}} \cdot \epsilon \tag{5}$$

这使得细化器学会从退化信号中恢复高质量帧，而非简单地上采样。

**前缀潜在参考策略**：为保持身份一致性和运动连贯性，细化器采用分块生成策略。对于每个新块，其前 $m$ 帧取自上一块的最后 $m$ 帧作为干净参考，仅对未来帧注入噪声：

$$z_{i,t}^{\mathrm{hr}} = \begin{cases} z_i^{\mathrm{hr}}, & 0 \leq i \leq m \\ (1-t) \cdot \epsilon_i + t \cdot z_i^{\mathrm{hr}}, & m < i \leq f \end{cases} \tag{6}$$

对应的训练目标仅在未来帧上计算速度预测误差，通过掩码 $w_i$ 排除前缀帧：

$$\mathcal{L}_{\mathrm{ref}} = \mathbb{E}_{\epsilon_i \sim \mathcal{N}(0,I), t \sim \mathcal{U}(0,1)} \mathbf{w} \cdot \| f_{\theta}(\{z_{i,t}^{\mathrm{hr}}\}_{i=0}^f, z^{\mathrm{deglr}}, P', I_{\mathrm{ref}}) - \{z_{i,1}^{\mathrm{hr}} - \epsilon_i\}_{i=0}^f \|_2^2 \tag{7}$$

$$w_i = \begin{cases} 1, & i > m \\ 0, & \text{otherwise} \end{cases} \tag{8}$$

其中 $P'$ 为姿态引导条件。该设计确保模型以前缀帧为视觉锚点，在保持身份一致性的同时生成连贯的未来运动。消融实验证实，去除 PG-Refiner 导致 FID 从 91.74 升至 109.54，FSIM 从 0.88 降至 0.79（Table 2），验证了该模块对视频质量和身份保持的关键作用。

### 3.3 手部特定奖励反馈学习

现有方法普遍忽视手部建模，导致手势失真和与音频的不对齐。InfinityHuman 引入基于奖励反馈的手部优化机制：利用预训练的手部质量奖励模型 $r_{\mathrm{hand}}$，对随机采样的解码帧 $X_i^{\mathrm{lr}}$ 进行质量评估，并以奖励差异作为优化目标：

$$\mathcal{L}_{\mathrm{hand}}(\theta) = \mathbb{E}_{c \sim p(c)} \mathbb{E}_{X_i^{\mathrm{lr}} \sim \mathcal{D}(z_{i,1}^{\mathrm{lr}})} \left[ T - r_{\mathrm{hand}}(X_i^{\mathrm{lr}}, c) \right] \tag{9}$$

其中 $T$ 为目标奖励阈值，$c$ 为条件信息。该损失直接优化生成器参数 $\theta$，使模型在训练中主动减少手部畸变。消融实验表明，去除该机制导致手部关键点精度 HKC 从 0.87 降至 0.85（Table 2），证实了其对提升手部生成质量的有效性。

### 模块间协同关系

四个模块形成递进式协同：LR-A2V 提供粗粒度的音画对齐运动基元；PG-Refiner 以姿态序列为无漂移几何引导，以前缀帧为身份锚点，将低分辨率输出恢复为高保真长视频；手部奖励反馈学习作为细粒度校正，专门修复细小关节的失真；多模态交叉注意力则贯穿第一阶段，从源头增强音频-视觉的对齐精度。这一由粗到细、从全局到局部的设计，使 InfinityHuman 在长时生成中有效抑制了误差累积。

### 补充图表

![[assets/figures/papers/paper_list_l1066_https_openaccess_thecvf_com_content_CVPR2026_html_Li_InfinityHuman_Towar/figures/002_Figure_2.jpg]]
*Figure 2: Progressive Degradation in Long Video Animation by Previous Methods. Existing methods suffer from cumulative errors leading to pronounced identity drift (facial inconsistencies), color shifts (hair, clothing), scene instability (background fluctuations), and hand motion artifacts. These challenges underscore the necessity of InfinityHuman’s pose-guided refiner and hand-specific optimization for producing high-fidelity, temporally coherent animations over extended sequences*



## 实验与关键发现

### 实验设置

InfinityHuman 在 **EMTD** 和 **HDTF** 两个公开数据集上进行训练与评估，涵盖长时间演讲、访谈及多样化动作场景。训练采用多条件随机丢弃策略以增强鲁棒性：文本和音频条件以 10% 概率独立丢弃，参考图像和首帧以 10% 概率联合丢弃；在姿态引导细化器（Pose-Guided Refiner）训练中，姿态和低分辨率潜在表示以 20% 概率丢弃。评估指标覆盖视频质量（FID↓、FVD↓、IQA↑）、身份保持（FaceSIM↑）、唇形同步（ASE↓、Sync-C↑）、手部精度（HKC↑）及结构相似性（FSIM↑）。基准方法包括 **HunyuanVideo-Avatar**（Chen et al., arXiv 2025）、**Hallo3**（Cui et al., CVPR 2025）、**OmniAvatar**（Gan et al., arXiv 2025）、**Let Them Talk**（Kong et al., arXiv 2025）、**OmniHuman-1**（Lin et al., ICCV 2025）和 **FantasyTalking**（Wang et al., ACM Multimedia 2025），其中标注 ∗ 的方法仅支持头部动画。

### 主结果

Table 1 给出了 EMTD 和 HDTF 上的定量对比。InfinityHuman 在视频质量和唇形同步指标上均取得最优结果：在 EMTD 上，FID 为 69.28，FVD 为 239.05，IQA 为 2.11，ASE 为 1.22；在 HDTF 上，FID 为 60.71，FVD 为 979.88，IQA 为 2.48，ASE 为 1.59。身份保持方面，FaceSIM 达到 0.84（EMTD）；手部精度 HKC 达到 0.90（HDTF）。值得注意的是，InfinityHuman 在 FVD 上相比头部动画方法（如 Hallo3）和全身动画方法（如 OmniHuman-1）均有显著领先，证明两阶段由粗到细框架在长时运动连贯性上的优势。

![[assets/figures/papers/paper_list_l1066_https_openaccess_thecvf_com_content_CVPR2026_html_Li_InfinityHuman_Towar/figures/004_Table_1.jpg]]
*Table 1: Quantitative Comparison of Audio-Driven Animation Methods on EMTD and HDTF. ∗ denotes methods limited to talkinghead animation. InfinityHuman achieves SOTA results across benchmarks.(§4.2)*

Figure 4 的定性对比进一步验证了数值结果：黄色框标注的手部畸变和蓝色框标注的面部身份不匹配在基准方法中明显存在，而 InfinityHuman 在长时生成中保持了身份一致性和唇形同步精度，手部姿态更自然、手势更丰富。

![[assets/figures/papers/paper_list_l1066_https_openaccess_thecvf_com_content_CVPR2026_html_Li_InfinityHuman_Towar/figures/006_Figure_4.jpg]]
*Figure 4: Qualitative Results of Audio-Driven Animation Methods on EMTD. Yellow and blue boxes highlight hand distortions and face ID mismatches, respectively. The results demonstrate the superiority of InfinityHuman in maintaining identity consistency, lip-sync accuracy, and visual fidelity during long-duration generation. Please zoom in for details. (§4.2)*

### 消融实验

Table 2 报告了关键组件的消融结果，所有实验在子集数据集上进行。

**姿态引导细化器（Pose-Guided Refiner）** 是核心贡献。去除该模块后，FID 从 91.74 升至 109.54（↑17.8），FSIM 从 0.88 降至 0.79（↓0.09），表明解耦的姿态序列作为稳定几何控制信号有效抑制了长时生成中的身份漂移和颜色偏移。进一步消融细化器的内部条件：去除低分辨率视频潜在条件（LR video latent condition）或姿态引导条件（pose guidance condition）均导致质量下降，验证了退化低分辨率潜在表示（Eq. (5) 中的 $z^{\mathrm{deglr}}$）和姿态序列作为无漂移引导信号的必要性。

**手部特定奖励反馈学习** 对精细关节建模有明确贡献。去除该模块后，手部关键点精度 HKC 从 0.87 降至 0.85（↓0.02）。虽然降幅看似微小，但在手部区域占比较小的全身动画场景中，这一差异对应着可感知的手势失真改善（见 Figure 5 可视化）。该结果验证了 Eq. (9) 中基于预训练手部质量奖励模型 $r_{\mathrm{hand}}$ 的反馈机制能有效纠正细小关节畸变。

### 长时稳定性评估

Table 3 报告了从 10s 到 50s 的累计指标变化，这是验证长时生成能力的核心证据。随着时长增加，FID 从 36.83 变为 35.50，FVD 从 1015.36 变为 945.84，FSIM 从 0.8357 变为 0.8057，Sync-C 从 7.23 变为 7.46。所有指标保持稳定，无显著退化趋势。这一结果直接支持了核心洞察：姿态序列结构上不受外观退化影响，配合参考帧作为视觉锚点，能够在长时间跨度内维持身份一致性和运动连贯性。

![[assets/figures/papers/paper_list_l1066_https_openaccess_thecvf_com_content_CVPR2026_html_Li_InfinityHuman_Towar/figures/008_Table_3.jpg]]
*Table 3: Long-Form Video Stability Evaluation. Cumulative metrics over increasing durations on the subset dataset*

### 失败模式与局限性

尽管整体性能领先，InfinityHuman 存在以下已知局限：① 训练数据仅包含单人连续视频，导致模型无法处理多人交互和场景切换（如镜头剪切或转场），这限制了其在对话场景或多人表演中的应用；② 在极端手部姿态（如高度遮挡或罕见手势）下，手部奖励模型可能无法提供有效反馈，生成质量仍有提升空间。这些失败模式提示未来工作需探索多人条件建模和更鲁棒的手部表示。

### 图表结论摘要

- **Table 1**：InfinityHuman 在 EMTD 和 HDTF 上全面达到 SOTA，尤其在 FVD（运动连贯性）和 HKC（手部精度）上优势明显。
- **Figure 4**：定性结果直观展示了 InfinityHuman 在身份保持、唇形同步和手部自然度上相比基准方法的显著提升。
- **Table 2**：消融实验证实姿态引导细化器和手部奖励反馈是不可或缺的组件，去除后 FID 上升 17.8、HKC 下降 0.02。
- **Table 3**：10s 到 50s 的累计指标保持稳定，证明框架具备真正的长时生成能力，无误差累积导致的退化。

### 补充图表

![[assets/figures/papers/paper_list_l1066_https_openaccess_thecvf_com_content_CVPR2026_html_Li_InfinityHuman_Towar/figures/007_Figure_5.jpg]]
*Figure 5: Visualization of Ablation Study. Demonstrating the effects of key components on animation quality*

![[assets/figures/papers/paper_list_l1066_https_openaccess_thecvf_com_content_CVPR2026_html_Li_InfinityHuman_Towar/figures/001_Figure_1.jpg]]
*Figure 1: InfinityHuman is an audio-driven full-body animation framework that synthesizes long-duration videos with (a) temporally consistent visual appearance, (b) expressive and style-rich hand gestures, (c) dynamic human-object interactions, and (d) emotion-controllable, audio-aligned full-body motions*



## 定位与知识库关联

### 1. 与 baseline 的关系

InfinityHuman 定位为面向**长时音频驱动全身人体动画**的生成框架，其设计直接回应了现有方法在长视频生成中的两类系统性缺陷：**累积误差导致的身份漂移与视觉退化**，以及**手部运动建模缺失**。

在方法谱系中，InfinityHuman 与以下基线形成明确对比：

- **HunyuanVideo-Avatar** (Chen et al., arXiv 2025)、**OmniAvatar** (Gan et al., arXiv 2025)、**Let Them Talk** (Kong et al., arXiv 2025) 等全身动画方法：这些方法采用单阶段直接生成策略，以先前运动帧作为时序条件。随着生成时长增加，误差在自回归过程中逐步累积，导致面部身份不一致、颜色偏移和背景不稳定（见 Figure 2 所示退化现象）。InfinityHuman 通过**两阶段由粗到细框架**和**解耦姿态序列作为无漂移引导信号**，从根本上切断了外观退化在时序上的传播路径。

- **Hallo3** (Cui et al., CVPR 2025)、**FantasyTalking** (Wang et al., ACM Multimedia 2025) 等头部动画方法：这些方法局限于头部区域生成，缺乏全身运动建模能力，更未涉及手部精细控制。InfinityHuman 通过引入**手部特定奖励反馈学习**，首次将手部关键点精度纳入优化目标，弥补了该空白。

- **OmniHuman-1** (Lin et al., ICCV 2025)：同为全身动画方法，但其未采用姿态解耦策略，也未专门优化手部区域。InfinityHuman 在 EMTD 和 HDTF 基准上的 FID、FVD、HKC 等指标均达到 SOTA 水平，验证了姿态引导细化器和手部奖励机制的增益。

### 2. 核心差异机制

InfinityHuman 与基线方法的本质差异体现在以下五个关键设计槽位：

| 设计槽位 | 基线取值 | InfinityHuman 取值 | 机制作用 |
|---------|---------|-------------------|---------|
| 整体框架 | 单阶段直接生成 | 两阶段由粗到细（LR-A2V + PG-Refiner） | 将运动生成与外观细化解耦，阻断误差累积 |
| 时序条件信号 | 先前运动帧 | 解耦姿态序列 + 参考帧锚点 | 姿态序列结构上不受外观退化影响，提供稳定几何引导 |
| 手部建模 | 无专门优化 | 手部特定奖励反馈学习 + 高质量手部数据 | 通过预训练奖励模型显式纠正手部畸变 |
| 音频条件注入 | 融合交叉注意力 | 解耦多模态交叉注意力（独立音频分支） | 增强音画对齐精度，避免文本与音频条件相互干扰 |
| 参考帧处理 | 结构对齐参考网络 | 前缀潜在参考策略 | 以初始帧潜在表示作为身份锚点，维持长期一致性 |

其中，**姿态引导细化器（Pose-Guided Refiner）** 是阻断累积误差的核心因果旋钮：消融实验表明，移除该模块导致 FID 从 91.74 升至 109.54，FSIM 从 0.88 降至 0.79（Table 2），证实了姿态序列作为无漂移控制信号的有效性。**手部奖励反馈学习**则针对细小关节畸变提供精细化纠正：移除该机制使 HKC 从 0.87 下降至 0.85（Table 2），虽降幅较小，但在定性结果中手部畸变的改善显著（Figure 4）。

### 3. 适用边界与局限

InfinityHuman 的适用边界由其训练数据分布和框架设计共同界定：

- **训练数据限制**：模型仅在**单人连续视频**上训练，因此当前框架**无法处理多人交互场景和复杂场景过渡**（如镜头切换、剪切）。这是论文明确指出的核心局限（§Limitations）。

- **姿态估计依赖**：两阶段流程依赖外部姿态估计器提供姿态序列。当输入音频对应的运动模式超出姿态估计器的分布（如极端杂技动作），姿态引导的质量可能下降，进而影响细化器输出。

- **手部奖励模型的覆盖范围**：手部奖励模型基于预训练数据集构建，对**极端手部姿态**（如高度遮挡、非自然手势）的奖励信号可能不够准确，导致该类场景下手部质量提升有限。这是一个开放问题。

- **推理效率**：姿态细化器通过蒸馏为 1 步模型实现高效推理，但两阶段流程相比单阶段方法仍存在额外计算开销。论文未提供与单阶段方法的推理时间对比，该点需查阅代码仓库验证。

### 4. 开放问题与后续方向

基于 InfinityHuman 的当前设计，以下方向值得后续工作探索：

1. **多人交互与场景切换**：如何将姿态引导和身份锚点机制扩展至多人场景？多人场景中身份锚点的定义和姿态序列的解耦方式需要重新设计。

2. **极端手部姿态的生成质量**：当前手部奖励模型的训练数据可能未充分覆盖极端姿态。引入手部物理约束或 3D 手部先验可能是提升鲁棒性的路径。

3. **与 3D 人体先验的融合**：InfinityHuman 使用 2D 姿态序列作为引导信号，但未显式利用 3D 人体模型（如 SMPL-X）。融合 3D 先验可能进一步提升运动连贯性和物理合理性。

4. **实时或低延迟推理**：当前两阶段流程虽通过蒸馏实现高效推理，但实时应用场景（如虚拟主播）对延迟有更高要求。进一步压缩模型或设计单阶段等价模型是工程化方向。

5. **跨身份泛化**：参考帧作为身份锚点的策略在训练身份与推理身份一致时效果最佳。对于零样本跨身份生成场景，前缀潜在参考策略的泛化能力需要进一步验证。



## 原文 PDF

![[paperPDFs/CVPR_2026/InfinityHuman_Towards_Long_Term_Audio_Driven_Human_Animation.pdf]]

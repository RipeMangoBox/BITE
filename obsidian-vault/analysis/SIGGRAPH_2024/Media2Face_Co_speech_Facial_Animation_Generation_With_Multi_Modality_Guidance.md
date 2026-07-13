---
title: "Media2Face: Co-speech Facial Animation Generation With Multi-Modality Guidance"
type: paper
paper_level: A
venue: SIGGRAPH
year: 2024
pdf_ref: paperPDFs/SIGGRAPH_2024/Media2Face_Co_speech_Facial_Animation_Generation_With_Multi_Modality_Guidance.pdf
project_link: https://sites.google.com/view/media2face
code_link: null
aliases:
- Media2Face
tags:
- SIGGRAPH_2024
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: "通过构建大规模、多样化、带有情感与风格标注的4D面部动画数据集（M2F-D），并在解耦身份的表达潜空间（GNPFA）中利用扩散模型联合生成表情和头部姿态，同时融合音频、文本、图像多模态引导，从根本上提升了生成的保真度与可控性。"
primary_logic: "学习一个通用的、非线性的人脸表情潜空间（GNPFA），能够从普通视频中提取接近于扫描级别的高质量表情和头部姿态，进而为扩散模型提供充足且精准的训练数据；同时，利用多条件无分类器引导策略在扩散过程中解耦语音与风格，使生成的面部动画兼具精确的唇音同步和丰富的情感/风格表现力。"
claims:
- "GNPFA提供的高质量数据与表达潜空间对生成精度至关重要，移除GNPFA导致LVE从10.44显著恶化至14.89。"
- "多条件无分类器引导（CFG）有效提升生成质量，无CFG时FDD从12.21大幅升高至16.69。"
- "Media2Face在M2F-D测试集的主要指标LVE、FDD、BA上全面超越现有所有基线方法。"
- "用户研究显示，在一般场景、无风格提示及无风格提示且无头部姿态的情况下，用户对Media2Face的偏好率分别超过90%、80%和70%，在唱歌场景中优势尤其明显。"
---

# Media2Face: Co-speech Facial Animation Generation With Multi-Modality Guidance

> [!tip] 核心洞察
> 学习一个通用的、非线性的人脸表情潜空间（GNPFA），能够从普通视频中提取接近于扫描级别的高质量表情和头部姿态，进而为扩散模型提供充足且精准的训练数据；同时，利用多条件无分类器引导策略在扩散过程中解耦语音与风格，使生成的面部动画兼具精确的唇音同步和丰富的情感/风格表现力。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | Media2Face：基于多模态引导的协同语音面部动画生成 |
| 英文题名 | Media2Face: Co-speech Facial Animation Generation With Multi-Modality Guidance |
| 会议/期刊 | SIGGRAPH 2024 |
| Links | [paper](https://arxiv.org/abs/2401.15687) · [Project](https://sites.google.com/view/media2face) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | Media2Face |
| Dataset | M2F-D, M2F-D (all metrics) |

> [!tip] 效果简介
> - M2F-D 上，LVE (mm) 为 10.44，对比 14.89 (Ours w/o GNPFA)，变化 -4.45。
> - M2F-D 上，FDD (×10^{-5} m) 为 12.21，对比 16.69 (Ours w/o CFG)，变化 -4.48。
> - M2F-D 上，BA 为 0.254，对比 —，变化 —。

## 概要

协同语音的面部动画生成（Co-speech Facial Animation）旨在根据输入的语音信号合成同步、自然且富有表现力的3D面部运动。该领域的核心瓶颈在于：高质量4D面部数据与丰富多模态标注（情感、风格）的稀缺，导致现有方法在动画真实感、条件控制的灵活性以及头部姿态与表情的协调性方面均存在明显不足。

针对上述瓶颈，本文提出 **Media2Face**，其核心思路可概括为“更好的数据、更好的表示、更好的生成”。首先，作者构建了一个大规模、多样化且带有情感与风格标注的4D面部动画数据集 **M2F-D**，为模型训练提供了关键的数据基础。其次，提出了**广义神经参数化面部资产（GNPFA）**——一个解耦身份的表达潜空间变分自编码器，能够从普通视频中提取接近扫描级别的高质量表情与头部姿态，为扩散模型提供精准且充足的训练数据。最后，在GNPFA潜空间中设计了一个扩散模型，以音频、文本、图像作为多模态条件，联合生成表情与头部姿态，并通过多条件无分类器引导策略解耦语音内容与风格表现。

实验结果表明，Media2Face在M2F-D测试集上的主要指标（唇音同步误差LVE、面部动态偏差FDD、双模对齐度BA）全面超越现有基线方法。消融实验证实：移除GNPFA导致LVE从10.44恶化至14.89，移除无分类器引导（CFG）使FDD从12.21升高至16.69，验证了高质量表达潜空间与多条件引导策略的决定性作用。用户研究进一步显示，在一般场景、无风格提示及无头部姿态的条件下，用户对Media2Face的偏好率分别超过90%、80%和70%，在唱歌场景中优势尤为显著。



### 问题背景

生成与语音高度同步、且富有表现力的三维面部动画是数字人、影视制作和虚拟交互中的核心挑战。一段自然的协同语音面部动画不仅需要精确的唇音同步，还要求面部表情、头部姿态与语音的韵律、情感和风格协调一致。然而，现有方法在生成质量、可控性以及数据基础三个层面均面临显著瓶颈。

### 现有方法缺口

**数据稀缺与标注匮乏** 是制约该领域发展的根本瓶颈。高质量的四维面部扫描数据获取成本极高，而来自普通视频的三维重建数据又缺乏情感、风格等细粒度标注。如 Table 1 所示，现有公开数据集在规模、多样性和标注丰富度上均存在明显不足——例如，DiffposeTalk 仅组合了重建的 TFHP 与 HDTF 数据，EMOTE 则基于重建的 MEAD 进行训练。这种数据层面的局限直接导致两个后果：其一，训练出的模型难以捕捉面部运动的细微变化，生成的动画真实感有限；其二，缺乏灵活的条件控制手段，用户无法按需指定情感或风格。

**面部表示与头部姿态的割裂** 是方法层面的突出缺陷。主流方案（如 FaceFormer、CodeTalker、FaceDiffuser）通常基于三维可变形模型参数或 blendshape 权重的线性空间来表示表情，这类表示对细微运动的刻画能力不足。更为关键的是，绝大多数方法要么完全忽略头部姿态的生成，要么将其作为独立的后处理步骤，导致表情与头部运动之间缺乏自然协调——这正是 Table 2 中 FaceFormer、CodeTalker、FaceDiffuser 和 EmoTalk 不适用 BA 指标的原因：它们根本不生成头部姿态。

**条件模态单一** 进一步限制了生成的可控性。现有工作几乎仅以音频作为唯一的驱动信号。情感感知方法如 EmoTalk 虽然尝试从音频中提取情感特征，但这种隐式提取无法由用户显式指定，且对唱歌等情感表达丰富的场景适应性差。当需要生成特定风格或情感的面部动画时，纯音频条件显然不足以提供充分的控制维度。

### 本文动机

针对上述三重缺口，本文的核心动机在于：**构建一个从数据基础到表示空间再到生成范式的系统性解决方案**。具体而言：

1. **数据层面**：通过设计一种能够从普通视频中提取接近扫描级精度的面部表情和头部姿态的神经表示，打破对昂贵四维扫描数据的依赖，从而构建大规模、多样化且带有情感与风格标注的数据集 M2F-D。

2. **表示层面**：学习一个解耦身份的非线性表情潜空间 GNPFA，在顶点级粒度上统一编码表情几何与头部姿态，为扩散模型提供高质量、高信息密度的生成目标。

3. **生成与控制层面**：在 GNPFA 潜空间中构建扩散模型 Media2Face，融合音频、文本、图像三种模态作为条件，并通过多条件无分类器引导策略解耦语音内容与风格表达，使生成结果兼具精确的唇音同步与丰富的情感/风格表现力。



## 核心方法与创新机理

Media2Face 的核心创新并非单一技术点的堆砌，而是围绕“数据-表示-生成”三个环节的系统性重构，以突破现有方法在面部动画真实感与可控性上的瓶颈。其关键创新体现在以下四个维度：

### 1. 面部表示空间：从线性 3DMM 到非线性解耦潜空间

现有方法大多依赖 3DMM 参数或 blendshape 权重的线性组合来表示面部表情，这种表示的表达能力有限，难以捕捉细微的肌肉运动和非线性形变。Media2Face 提出了 **GNPFA（Generalized Neural Parametric Facial Asset）**，一个基于 VAE 的非线性表达潜空间。该空间的本质改进在于：它将身份信息与表情彻底解耦，使表情潜代码 $z_e$ 成为一个身份无关的、顶点级粒度的运动表示。这意味着，同一个表情潜代码可以驱动不同拓扑、不同身份的人脸模型生成高度个性化的动画（见 Figure 6），而无需为每个角色重新训练模型。这一表示空间的质量是后续所有模块的基础——消融实验表明，移除 GNPFA 直接导致唇音同步误差 LVE 从 10.44 恶化至 14.89（Table 2），充分证明了高精度表情潜空间对生成质量的决定性作用。

### 2. 头部姿态生成：从分离处理到联合建模

多数音频驱动面部动画方法（如 FaceFormer、CodeTalker、FaceDiffuser）完全忽略头部姿态，或将其作为独立的后处理步骤，导致表情与头部运动缺乏自然协调。Media2Face 将表情潜代码 $z_e^i$ 与头部姿态参数 $\theta^i$ 拼接为统一的“head motion code” $X^i$，在扩散模型的同一序列空间中联合生成。这种联合建模使模型能够学习语音信号与表情-头部姿态之间的耦合关系，从而产生更自然的整体运动。定量结果中 BA（Beat Align）指标达到 0.254（Table 2），而忽略头部姿态的基线方法在该指标上无法评估，从侧面验证了联合生成的必要性。

### 3. 条件模态：从单一音频到多模态引导

现有方法几乎仅以音频作为唯一的驱动条件，这严重限制了生成动画的风格可控性。Media2Face 将条件空间扩展为 **音频 + 文本提示 + 图像提示** 的三模态组合：音频特征由 Wav2Vec2 提取，文本/图像提示通过 CLIP 编码为条件潜码 $P$。这一设计使模型能够灵活地控制面部动画的情感与风格——用户可以通过文本描述（如“happy”或“sad”）或图像参考（如表情符号、抽象画作）来指定期望的表达风格，同时保持精确的唇音同步。在多条件无分类器引导（CFG）策略下，音频条件引导尺度 $s_A=2.5$ 和姿态条件引导尺度 $s_P=1.5$ 的独立设置，使得语音同步与风格表达可以在推理时解耦调节。消融实验证实，移除 CFG 后，面部动态偏差 FDD 从 12.21 显著恶化至 16.69（Table 2），证明了多条件引导策略的有效性。

### 4. 生成模型：从确定性回归到带运动正则的扩散模型

传统方法多采用 LSTM、Transformer 等确定性回归模型，或 VAE 等隐变量模型，这些方法在生成多样化、自然运动方面存在局限。Media2Face 采用 **Transformer 扩散模型**，直接预测干净的 head motion 序列 $\hat{X}_0^{1:N}$，并引入了两项运动正则化损失：

- **速度损失** $\mathcal{L}_{\mathrm{velocity}}$：约束预测序列与真实序列的帧间速度一致，公式为 $\mathcal{L}_{\mathrm{velocity}} = \| (X_0^{2:N} - X_0^{1:N-1}) - (\hat{X}_0^{2:N} - \hat{X}_0^{1:N-1}) \|_2^2$；
- **平滑损失** $\mathcal{L}_{\mathrm{smooth}}$：通过二阶差分惩罚突变，公式为 $\mathcal{L}_{\mathrm{smooth}} = \| \hat{X}_0^{3:N} + \hat{X}_0^{1:N-2} - 2\hat{X}_0^{2:N-1} \|_2^2$。

总训练损失为 $\mathcal{L} = \lambda_{\mathrm{simple}}\mathcal{L}_{\mathrm{simple}} + \lambda_{\mathrm{velocity}}\mathcal{L}_{\mathrm{velocity}} + \lambda_{\mathrm{smooth}}\mathcal{L}_{\mathrm{smooth}}$，权重分别为 1、1、0.01。这种设计使生成的动画既保持了扩散模型的多样性和高质量，又通过显式的运动约束保证了序列的自然流畅。

### 创新点的因果关联

上述四个创新并非孤立存在，而是形成了一条因果链路：GNPFA 提供的高质量表达潜空间使得从普通视频中提取接近扫描级精度的训练数据成为可能，进而支撑了大规模多模态数据集 M2F-D 的构建；充足且精准的数据又为扩散模型的训练提供了基础；而联合建模头部姿态与多模态条件引导则使模型能够生成兼具精确唇音同步和丰富情感/风格表现力的动画。这一链路的完整性是 Media2Face 在 LVE、FDD、BA 三项主要指标上全面超越所有基线方法（Table 2），并在用户研究中获得超过 90% 偏好率（Figure 5）的根本原因。



![[assets/figures/papers/paper_list_l38_https_arxiv_org_abs_2401_15687/figures/002_Figure_2.jpg]]
*Figure 2: GNPFA pipeline. (Left:) We train a geometry VAE to learn a latent space of expression and head pose, disentangling expression with identity. (Right:) Two vision encoders are trained to extract expression latent codes and head poses from RGB images, which enables us to capture a wide array of 4D data*

Media2Face 的整体流程由三大阶段串联而成：**表达潜空间构建（GNPFA）** → **大规模多模态数据采集（M2F-D）** → **条件扩散生成（Media2Face 扩散模型）**。三个阶段并非简单的流水线，而是形成了“数据飞轮”：GNPFA 提供了从普通视频提取高精度面部动画的能力，使得 M2F-D 数据集得以规模化构建；而 M2F-D 的丰富标注又为扩散模型提供了充足的训练信号，使多模态条件控制成为可能。

### 阶段一：GNPFA 表达潜空间

GNPFA（Generalized Neural Parametric Facial Asset）本质上是一个**解耦身份的非线性变分自编码器**，其核心目标是学习一个高泛化性的面部表情与头部姿态潜空间。与传统基于 3DMM 参数或 blendshape 权重的线性表示不同，GNPFA 直接在顶点级几何上操作，能够捕捉更精细的面部运动细节。

GNPFA 由三个子模块构成：
- **几何 VAE**：以中性几何为条件，采用 UNet 架构的生成器，将真实扫描数据或随机合成的 blendshape 几何编码为表达潜码 $z_e$，并重建为顶点级坐标图。训练时同时约束几何重建精度和潜码一致性。
- **映射网络 M 与 M'**：在 blendshape 权重空间与潜空间之间建立双向映射，使潜空间既具备物理可解释性，又能覆盖超出线性 blendshape 范围的丰富表情。
- **视觉表达编码器**：两个独立的编码器分别从 RGB 图像中提取表达潜码和头部姿态参数，使 GNPFA 能够从普通视频帧中恢复接近扫描级别的高质量 4D 面部数据。

### 阶段二：M2F-D 数据集构建

借助 GNPFA 的视觉编码器，研究者从大规模多样化视频中提取表情潜码和头部姿态，构建了 M2F-D 数据集。该数据集的核心优势在于：相比现有 4D 面部数据集，M2F-D 在数据量、说话人多样性、情感与风格标注丰富度上均有显著提升（见 Table 1）。这一阶段同时为下游扩散模型提供了训练所需的 ground-truth 序列——每帧由表达潜码 $z_e^i$ 与头部姿态 $\theta^i$ 拼接为统一的 **head motion code**。

### 阶段三：Media2Face 扩散模型

Media2Face 采用 Transformer 架构的**潜空间扩散模型**，直接在 head motion code 序列上进行去噪生成。其输入输出流如下：

1. **条件编码**：
   - 音频特征 $A^{1:N}$：由预训练 Wav2Vec2 提取，经线性插值对齐至动画序列长度。
   - 风格/情感潜码 $P$：由 CLIP 编码文本提示或图像提示得到，用于灵活控制表情风格。

2. **扩散去噪**：
   - 去噪网络 $\mathcal{G}$ 以噪声序列 $X_t^{1:N}$、时间步 $t$、音频特征 $A^{1:N}$ 和 CLIP 潜码 $P$ 为输入，直接预测干净的 head motion 序列 $\hat{X}_0^{1:N}$（类似 MDM 的 $x_0$-prediction 策略）。
   - 训练时对条件进行随机掩码，使模型学会在缺失部分条件时仍能合理生成，为推理时的**多条件无分类器引导（CFG）**奠定基础。

3. **推理采样**：
   - 使用 DDIM 确定性采样器从随机噪声逐步生成 head motion 序列。
   - 通过 CFG 尺度 $s_A=2.5$（音频引导）和 $s_P=1.5$（姿态/风格引导）解耦语音同步与风格表达，实现精确的唇音对齐同时保留丰富的情感表现力。
   - 对于超长音频，采用**重叠批处理去噪**策略，将音频分段并在重叠窗口内一次性完成去噪。

4. **几何解码**：
   - 生成的表达潜码送入 GNPFA 几何解码器，恢复为顶点级面部坐标图，再与模板网格结合得到最终面部几何。
   - 头部姿态参数直接应用于网格变换，实现表情与头部运动的自然协调。

### 关键设计决策与因果机制

框架的核心竞争力源于两个因果节点：

- **GNPFA 潜空间的质量直接决定生成精度**：消融实验表明，移除 GNPFA 改用传统 blendshape 表示后，唇音同步误差 LVE 从 10.44 急剧恶化至 14.89（Table 2），证实了高精度非线性表达潜空间是不可替代的基础设施。
- **多条件 CFG 是解耦语音与风格的关键**：移除 CFG 后，面部动态偏差 FDD 从 12.21 大幅升高至 16.69（Table 2），说明仅靠条件拼接无法有效平衡唇音精度与风格表现力，CFG 的引导机制在这一多目标权衡中起决定性作用。

此外，扩散模型的**速度损失** $\mathcal{L}_{\text{velocity}}$ 和**平滑损失** $\mathcal{L}_{\text{smooth}}$（权重分别为 1 和 0.01）通过约束帧间一阶和二阶差分，保证了生成序列的运动自然性和时间一致性，避免了纯 L2 重建损失可能产生的抖动或突变。



### GNPFA：泛化神经参数化面部资产

GNPFA 本质上是一个变分自编码器，旨在将面部几何与视频图像映射到统一的、解耦身份的表达潜空间。其核心包含三个子模块：

1. **几何 VAE**：由一个基于 UNet 的几何生成器 $\mathcal{G}_{\mathrm{geo}}$ 构成，以中性几何为条件，学习从表达潜码 $z_e$ 和头部姿态 $\theta$ 重构顶点级面部几何 $\mathbf{G}$。
2. **映射网络 $\mathcal{M}$ 与 $\mathcal{M}'$**：在 blendshape 权重 $w$ 与表达潜空间之间建立双向映射，使潜空间兼容传统的 blendshape 参数化表示。
3. **视觉表达编码器**：从 RGB 图像中提取表达潜码 $\hat{z}_e$ 与头部姿态 $\hat{\theta}$，为大规模 4D 数据采集提供桥梁。

#### 几何 VAE 的训练目标

训练数据包含两类：真实 4D 扫描数据与随机合成的 blendshape 数据。

**真实几何重建损失**（Section 3.1, Equation 1）：
$$\mathcal{L}_{\mathrm{recon,R}} = \| \tilde{\mathbf{G}}_{\mathrm{R}} - \mathbf{G}_{\mathrm{R}} \|_2^2$$
其中 $\tilde{\mathbf{G}}_{\mathrm{R}}$ 为解码器重建的几何，$\mathbf{G}_{\mathrm{R}}$ 为输入的真实扫描几何。该损失直接约束顶点级重建精度。

**Blendshape 合成数据重建损失**（Section 3.1, Equation 2）：
$$\mathcal{L}_{\mathrm{recon,B}} = \| \tilde{\mathbf{G}}_{\mathrm{B}} - \mathbf{G}_{\mathrm{B}} \|_2^2 + \| \tilde{z}_{\mathrm{B}} - z_{\mathrm{B}} \|_2^2 + \| \tilde{w}_{\mathrm{B}} - w_{\mathrm{B}} \|_2^2$$
此损失同时对几何、表达潜码和 blendshape 权重施加 L2 约束，确保潜空间与 blendshape 参数的一致性。

#### 视觉表达编码器的训练目标

为从 RGB 图像中提取表达信息，视觉编码器在两类数据上联合训练：

**真实图像监督损失**（Section 3.2）：
$$\mathcal{L}_{\exp,\mathrm{R}} = \| \hat{\mathbf{G}}_{\mathrm{R}} - \mathbf{G}_{\mathrm{R}} \|_2^2 + \| \hat{\mathbf{I}}_{\mathrm{R}} - \mathbf{I}_{\mathrm{R}} \|_2^2$$
其中 $\hat{\mathbf{G}}_{\mathrm{R}}$ 为由图像提取的潜码解码得到的几何，$\hat{\mathbf{I}}_{\mathrm{R}}$ 为渲染图像，$\mathbf{I}_{\mathrm{R}}$ 为输入的真实图像。该损失同时约束几何与图像层面的保真度。

**合成数据渲染损失**（Section 3.2）：
$$\mathcal{L}_{\exp,\mathrm{B}} = \| \hat{\mathbf{G}}_{\mathrm{B}} - \mathbf{G}_{\mathrm{B}} \|_2^2 + \| \mathcal{R}(\hat{\mathbf{G}}_{\mathrm{B}}, \hat{p}_{\mathrm{B}}) - \mathcal{R}(\mathbf{G}_{\mathrm{B}}, p_{\mathrm{B}}) \|_2^2$$
其中 $\mathcal{R}$ 为可微渲染器，$p$ 为相机参数。该损失利用渲染图像误差提供额外的监督信号，增强编码器对合成数据的泛化能力。

---

### Media2Face：多模态引导的潜空间扩散模型

Media2Face 是一个基于 Transformer 的潜空间扩散模型，在 GNPFA 表达潜空间中联合生成表情序列与头部姿态序列。其核心设计包括：

- **Head Motion Code**：将第 $i$ 帧的表达潜码 $z_e^i$ 与头部姿态 $\theta^i$ 拼接，形成单帧面部动画状态，序列记为 $\mathbf{X}^{1:N}$。
- **条件编码**：音频特征由预训练的 Wav2Vec2 提取并线性插值至动画序列长度，记为 $\mathbf{A}^{1:N}$；文本或图像提示由 CLIP 编码为条件潜码 $P$。
- **去噪网络 $\mathcal{G}$**：采用 Transformer 架构，以噪声序列 $\mathbf{X}_t^{1:N}$、时间步 $t$、音频特征 $\mathbf{A}^{1:N}$ 和 CLIP 潜码 $P$ 为输入，直接预测干净的 head motion 序列 $\hat{\mathbf{X}}_0^{1:N}$（与 MDM 的预测范式一致）。

#### 扩散模型的训练损失

**主损失 — Simple Loss**（Section 4.1）：
$$\mathcal{L}_{\mathrm{simple}} = \| \mathbf{X}_0^{1:N} - \hat{\mathbf{X}}_0^{1:N} \|_2^2$$
最小化预测序列与真实序列的 L2 距离，是扩散模型训练的核心目标。

**速度损失 — Velocity Loss**（Section 4.1）：
$$\mathcal{L}_{\mathrm{velocity}} = \| (\mathbf{X}_0^{2:N} - \mathbf{X}_0^{1:N-1}) - (\hat{\mathbf{X}}_0^{2:N} - \hat{\mathbf{X}}_0^{1:N-1}) \|_2^2$$
约束预测序列的帧间一阶差分与真实序列一致，确保运动速度的自然性，避免抖动。

**平滑损失 — Smooth Loss**（Section 4.1）：
$$\mathcal{L}_{\mathrm{smooth}} = \| \hat{\mathbf{X}}_0^{3:N} + \hat{\mathbf{X}}_0^{1:N-2} - \hat{\mathbf{X}}_0^{2:N-1} \|_2^2$$
通过惩罚预测序列的二阶差分（加速度），抑制突变，使生成的面部动画更加平滑流畅。

**总损失**（Section 4.1, 5.1）：
$$\mathcal{L} = \lambda_{\mathrm{simple}} \mathcal{L}_{\mathrm{simple}} + \lambda_{\mathrm{velocity}} \mathcal{L}_{\mathrm{velocity}} + \lambda_{\mathrm{smooth}} \mathcal{L}_{\mathrm{smooth}}$$
权重配置为 $\lambda_{\mathrm{simple}}=1$，$\lambda_{\mathrm{velocity}}=1$，$\lambda_{\mathrm{smooth}}=0.01$。平滑损失权重较小，仅作为正则项使用。

---

### 推理时的多条件无分类器引导

推理阶段采用 DDIM 确定性采样，并引入多条件无分类器引导（CFG）以解耦语音与风格控制。去噪预测公式为：
$$\hat{\mathbf{X}}_0^{1:N} = \mathcal{G}(\mathbf{X}_t^{1:N}, t, \mathbf{A}^{1:N}, P)$$

CFG 引导尺度设置为 $\mathbf{s}_A = 2.5$（音频条件）和 $\mathbf{s}_P = 1.5$（姿态/风格条件），通过随机掩码条件并在推理时外推，实现对唇音同步精度与风格表现力的灵活权衡。消融实验（Table 2, Ours w/o CFG）证实，移除 CFG 后 FDD 从 12.21 恶化至 16.69，验证了该策略的有效性。



## 实验与关键发现

### 核心瓶颈与验证逻辑

Media2Face 的实验设计围绕一个中心因果链条展开：**高保真面部动画的根本瓶颈在于缺乏高质量、大规模、带多模态标注的 4D 数据，以及缺乏能解耦身份、精准表达面部细节的通用潜空间**。实验通过三个层次验证这一逻辑：(1) 在自建数据集 M2F-D 上全面超越现有基线；(2) 通过消融实验证明 GNPFA 潜空间与多条件无分类器引导 (CFG) 各自的决定性贡献；(3) 通过用户研究验证生成结果在感知层面的压倒性优势，尤其在情感表达丰富的唱歌场景中。

### 主实验结果

Table 2 报告了在 M2F-D 测试集上的定量对比。Media2Face 在所有主要指标上全面超越现有基线方法。

![[assets/figures/papers/paper_list_l38_https_arxiv_org_abs_2401_15687/figures/006_Table_2.jpg]]
*Table 2: Quantitative comparisons and evaluations. Notice that the BA metric is not utilized for FaceFormer, CodeTalker, FaceDiffuser, and EmoTalk, as they do not generate head poses. Also, metrics related to vertices are not utilized for SadTalker due to its different facial topology*

**唇音同步精度 (LVE)**：Media2Face 取得 10.44 mm 的唇部顶点误差，显著优于 FaceDiffuser、EmoTalk 等扩散基线及 FaceFormer、CodeTalker 等确定性回归方法。LVE 直接测量生成唇形与真实扫描唇形的几何偏差，是衡量语音驱动精度的核心指标。

**面部动态保真度 (FDD)**：Media2Face 取得 $12.21 \times 10^{-5}$ m 的面部动态偏差，表明生成的表情运动轨迹与真实数据高度一致。FDD 衡量的是顶点运动序列的分布差异，能捕捉到帧间动态的细微失真。

**头部姿态对齐度 (BA)**：Media2Face 取得 0.254 的双目对齐误差。由于 FaceFormer、CodeTalker、FaceDiffuser 和 EmoTalk 本身不生成头部姿态，该指标仅对 DiffposeTalk 等生成头部姿态的方法具有可比性。Media2Face 在该指标上的优势验证了联合生成表情与头部姿态策略的有效性。

> **公平性说明**：Table 2 明确标注，BA 指标不适用于不生成头部姿态的方法；SadTalker 因使用不同面部拓扑，不适用基于顶点距离的 LVE 和 FDD。所有方法使用相同的数据划分与预处理流程，音频编码器保持一致。

### 消融实验：因果机制的实证拆解

Table 2 中的消融实验直接验证了论文核心主张的因果机制。

**移除 GNPFA 的致命影响**：当用传统 blendshape 参数替代 GNPFA 表达潜空间时，LVE 从 10.44 急剧恶化至 14.89。这一 4.45 mm 的退化幅度远超各基线之间的差异，确凿地证明：**GNPFA 提供的解耦身份、顶点级粒度的非线性表达潜空间，以及基于该潜空间提取的高质量训练数据，是生成精度的根本保障**。传统线性 blendshape 空间无法捕捉真实面部运动的细微变化，导致唇音同步和表情细节的双重损失。

**移除多条件无分类器引导 (CFG) 的显著退化**：当禁用 CFG 策略时，FDD 从 12.21 大幅升高至 16.69。这验证了多条件引导策略在扩散过程中解耦语音与风格的核心作用——没有 CFG，音频条件与 CLIP 风格条件之间的干扰会导致面部动态失真，表现为运动轨迹偏离真实分布。

**数据规模的正向驱动**：Table 2 中报告了训练数据规模消融，结果表明随着 M2F-D 数据集规模的扩大，FDD 和 BA 指标持续改善。这直接证明了 M2F-D 数据集本身的价值——更大规模、更多样化的 4D 面部动画数据为扩散模型提供了更丰富的运动先验。

### 用户研究：感知层面的压倒性优势

Figure 5 报告了用户研究结果，从人类感知维度验证生成质量。在三个测试场景中，用户对 Media2Face 的偏好率均呈现压倒性优势：

![[assets/figures/papers/paper_list_l38_https_arxiv_org_abs_2401_15687/figures/008_Figure_5.jpg]]
*Figure 5: User study result. Note how our method has demonstrated overwhelming superiority in the singing cases, showcasing the model’s ability to generate rich emotions and rhythmic head movements*

- **一般场景**：偏好率超过 90%；
- **无风格提示场景**：偏好率超过 80%；
- **无风格提示且无头部姿态场景**：偏好率超过 70%。

尤其值得关注的是**唱歌场景**中的表现——Media2Face 在该场景下展现出远超基线方法的优势。这一结果直接验证了模型生成丰富情感表达和节奏性头部运动的能力，也间接证明了多模态条件（尤其是 CLIP 文本/图像引导）在控制情感与风格方面的有效性。

### 定性结果与泛化能力

Figure 6 展示了将生成动画重定向到不同身份的结果。得益于 GNPFA 的身份解耦特性，同一段生成的表情序列可以适配不同性别、年龄、种族的面部模板，并产生个性化的面部细节（如不同的皱纹模式）。这表明 GNPFA 的表达潜空间具有高度的身份泛化性，为实际应用中的人物多样化提供了基础。

Figure 7 的定性对比进一步揭示了方法差异。与情感盲方法（FaceDiffuser 等）对比时，Media2Face 使用中性文本提示即可生成更自然的唇音同步；与情感感知方法（EmoTalk）对比时，Media2Face 通过文本提示灵活指定情感，而 EmoTalk 只能从音频中自动提取情感特征，无法手动控制。这凸显了多模态条件在可控性上的本质优势。

### 失败模式与开放挑战

论文未报告具体的失败案例或定量失败模式分析。从方法设计推断，潜在脆弱环节包括：(1) 极端抽象文本或图像提示可能无法通过 CLIP 编码为有效的风格控制信号，导致条件控制失效；(2) 长音频场景下，尽管采用了重叠批次去噪策略，时序一致性的保持仍是潜在挑战；(3) GNPFA 对训练时未见过的极端表情可能存在泛化不足。论文明确指出，**如何从更多样的多模态输入中实现忠实的条件控制仍是一个开放挑战**，这需要进一步的实证研究来验证。

### 补充图表

![[assets/figures/papers/paper_list_l38_https_arxiv_org_abs_2401_15687/figures/003_Table_1.jpg]]
*Table 1: 4D datasets comparison. Notice that DiffposeTalk [57] is a combination of reconstructed TFHP [57] and HDTF. EMOTE [15] is trained on reconstructed MEAD*



## 定位与知识库关联

Media2Face 的核心贡献在于构建了一个**解耦身份的非线性表达潜空间（GNPFA）**，并在该空间中利用**多模态条件扩散模型**联合生成表情与头部姿态。这一设计使其在方法谱系中处于“音频驱动面部动画生成”与“多模态可控生成”的交汇点，并对现有基线形成了系统性的替代与超越。

### 与音频驱动面部动画方法的对比与定位

现有音频驱动面部动画方法普遍依赖 **3DMM 参数或 blendshape 权重的线性表示**来驱动面部运动，这构成了它们与 Media2Face 之间最根本的差异。具体而言：

- **FaceFormer** 与 **CodeTalker** 分别采用 Transformer 自回归和离散运动先验进行音频到面部运动的确定性映射，但它们均不生成头部姿态，且其线性 blendshape 空间难以捕捉顶点级的细微表情变化（如皱纹）。Media2Face 的 GNPFA 潜空间提供了**顶点粒度的非线性表达**，并通过联合生成头部姿态序列，在唇音同步精度（LVE）和运动自然度（FDD）上形成了显著优势（Table 2）。

- **FaceDiffuser** 虽引入了扩散模型，但其操作空间仍为线性参数空间，且条件模态仅限于音频。Media2Face 将扩散过程迁移至 GNPFA 潜空间，并引入 **Wav2Vec2 音频特征与 CLIP 文本/图像特征的多条件交叉注意力机制**，实现了风格与情感的灵活注入。

- **EmoTalk** 是少数具备情感感知能力的基线，但其情感特征从音频中隐式提取，无法由用户显式指定。Media2Face 通过 CLIP 编码的文本或图像提示实现了**显式、可编辑的风格控制**，用户可逐帧指定情感标签（Figure 4），这一定性差异在用户研究中体现为压倒性的偏好率（Figure 5）。

- **DiffposeTalk** 同样采用扩散模型生成表情与头部姿态，但其训练数据受限于重建质量。Media2Face 的 GNPFA 从普通视频中提取**接近扫描级别的高质量 4D 数据**（M2F-D 数据集），为扩散模型提供了更精准的监督信号，这是其性能优势的关键数据基础（Table 1, Table 2 消融）。

- **SadTalker** 使用不同的面部拓扑，因此无法直接进行顶点级指标对比，但其 2D/3D 混合范式与 Media2Face 的全 3D 顶点动画路径存在本质差异。

### 核心设计决策的因果机制

Media2Face 的性能优势可归因于两个相互依赖的设计决策，消融实验提供了明确的因果证据：

1. **GNPFA 表达潜空间作为数据与生成的基础设施**：GNPFA 不仅是一个几何 VAE，它通过解耦身份与表情，使得从普通视频中提取高精度 4D 标注成为可能，从而构建了大规模、多样化的 M2F-D 数据集。移除 GNPFA 导致 LVE 从 10.44 急剧恶化至 14.89（Table 2），证明**高质量的表达潜空间与相应的训练数据是生成精度的必要条件**。

2. **多条件无分类器引导（CFG）作为风格与语音的解耦机制**：扩散模型在训练时随机掩码音频或 CLIP 条件，推理时通过独立的引导尺度（$s_A=2.5$，$s_P=1.5$）分别控制唇音同步和风格强度。移除 CFG 使 FDD 从 12.21 大幅升高至 16.69（Table 2），表明**多条件引导策略是平衡语音忠实度与风格表现力的关键**。

### 适用边界与局限

尽管 Media2Face 在定量指标和用户偏好上均表现优异，其方法仍存在明确的适用边界：

- **数据依赖性**：GNPFA 的预训练依赖高质量面部扫描数据，M2F-D 的构建依赖视觉编码器从视频中提取表达的能力。在极端姿态、遮挡或低分辨率视频场景下，表达提取的精度可能下降，进而影响生成质量。论文未提供此类退化场景下的鲁棒性分析。

- **多模态控制的忠实度**：论文明确指出，从更抽象或多样化的文本/图像输入中实现忠实的条件控制仍是一个开放挑战。CLIP 潜码虽能传递高层语义风格，但对细粒度、组合式情感的控制能力未经系统验证。

- **实时性与计算开销**：扩散模型的迭代采样与 Transformer 去噪器的推理成本未与轻量级回归方法（如 FaceFormer）进行对比。对于要求低延迟的实时应用，其适用性需要进一步评估。

### 开放问题

- **多模态条件解耦的粒度**：当前 CFG 策略将音频和 CLIP 条件作为两个整体进行引导，但 CLIP 潜码内部可能混杂风格、情感、身份等多种语义。如何实现更细粒度的条件解耦与控制，是提升生成可控性的关键方向。

- **跨身份泛化的上限**：GNPFA 解耦了身份与表情，但扩散模型在训练时仍与特定身份的数据分布相关。在极端跨身份迁移（如从成人到儿童）时，生成的运动模式是否保持自然，尚待验证。



## 原文 PDF

![[paperPDFs/SIGGRAPH_2024/Media2Face_Co_speech_Facial_Animation_Generation_With_Multi_Modality_Guidance.pdf]]

---
title: "EmoDiffTalk: Emotion-aware Diffusion for Editable 3D Gaussian Talking Head"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/EmoDiffTalk_Emotion_aware_Diffusion_for_Editable_3D_Gaussian_Talking_Head.pdf
project_link: "https://liuchang883.github.io/EmoDiffTalk/"
code_link: null
aliases:
- EmoDiffTalk
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 通过动作单元(AU)代码空间显式建模情感-表情映射，并将AU代码作为条件注入高斯扩散过程，从而调节三维高斯基元的动态属性。
primary_logic: 引入AU代码作为可解释的中间表示，既作为语音到表情的稀疏控制信号(AU提示扩散)，又作为文本到表情的编辑接口(文本到AU控制器)，实现细粒度、解耦的情感动画生成。
claims:
- 在EmoTalk3D数据集上，PSNR超过EmoTalk3D基线+4.56 dB，CPBD超过Hallo3基线+16.1%，LPIPS最低且LMD显著降低。
- 消融实验表明，移除AU代码对位置预测模块(Codes4P)或透明性预测模块(Codes4O)均导致PSNR大幅下降，验证了AU条件对精细动态建模的关键作用。
- 用户研究显示，文本驱动的情感编辑在视频真实感和情感控制上均超过Hallo3，验证了AU空间作为编辑接口的有效性。
- EmoTalk3D 上 PSNR = 25.78
---

# EmoDiffTalk: Emotion-aware Diffusion for Editable 3D Gaussian Talking Head

> [!tip] 核心洞察
> 引入AU代码作为可解释的中间表示，既作为语音到表情的稀疏控制信号(AU提示扩散)，又作为文本到表情的编辑接口(文本到AU控制器)，实现细粒度、解耦的情感动画生成。

| 字段 | 内容 |
|------|------|
| 中文题名 | EmoDiffTalk：面向可编辑3D高斯说话人头的情感感知扩散 |
| 英文题名 | EmoDiffTalk: Emotion-aware Diffusion for Editable 3D Gaussian Talking Head |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Liu_EmoDiffTalk_Emotion-aware_Diffusion_for_Editable_3D_Gaussian_Talking_Head_CVPR_2026_paper.html) · [Project](https://liuchang883.github.io/EmoDiffTalk/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | EmoDiffTalk |
| Dataset | EmoTalk3D, RenderMe-360 |

> [!tip] 效果简介
> - EmoTalk3D 上，PSNR 25.78 vs EmoTalk3D (21.22) (+4.56 dB)；CPBD 0.36 vs Hallo3 (0.31) (+16.1%)；LMD 3.56 vs lowest among compared methods (显著更低)。
> - RenderMe-360 上，LMD 6.59 vs Hallo3 (ca. 9.34) (-29.4%)；PSNR 21.41 vs Hallo3 (ca. 20.13) (+1.28 dB)。

## 概述

当前3D说话人头生成方法在实现精细且可扩展的多模态情感编辑方面存在明显瓶颈，情感到面部表情的映射往往较为模糊，难以通过文字或语音精确控制细粒度面部动作。针对这一问题，**EmoDiffTalk** 提出了一种面向可编辑3D高斯说话人头的情感感知扩散框架，其核心思想是通过动作单元（AU）代码空间显式建模情感-表情映射，并将AU代码作为条件注入高斯扩散过程，从而调节三维高斯基元的动态属性。

具体而言，该方法引入AU代码作为一种可解释的中间表示：一方面作为语音到表情的稀疏控制信号，通过AU提示扩散实现音频驱动的精细动画生成；另一方面作为文本到表情的编辑接口，通过文本到AU控制器实现细粒度、解耦的情感编辑。在技术实现上，EmoDiffTalk 采用三重平面特征网格替代传统球谐函数进行颜色外观获取，并构建了包含语音到AU编码器、AU提示高斯扩散、动态外观解码器和文本到AU情感控制器的完整管道。

实验结果表明，该方法在 EmoTalk3D 数据集上取得了显著优势：PSNR 达到 25.78 dB，较 EmoTalk3D 基线提升 4.56 dB；CPBD 达到 0.36，较 Hallo3 提升 16.1%；LPIPS 降至 0.12，LMD 降至 3.56，均为对比方法中的最优水平。在 RenderMe-360 数据集上，LMD 较 Hallo3 降低 29.4%，PSNR 提升 1.28 dB。消融实验进一步验证了AU代码对位置预测和不透明度预测模块的关键作用，以及扩散策略在捕捉运动分布方面的优势。用户研究亦表明，文本驱动的情感编辑在视频真实感和情感控制上均超过 Hallo3，证实了AU空间作为编辑接口的有效性。

## 背景与动机

三维说话人头生成旨在从语音信号合成逼真的动态面部动画，在虚拟现实、数字人交互、影视制作等领域具有广泛应用。近年来，基于3D高斯泼溅（3D Gaussian Splatting, 3DGS）的方法凭借其高质量渲染和自由视角能力，逐渐成为该领域的主流范式。然而，现有方法在**情感表达的可编辑性**方面存在显著不足，这构成了当前的核心瓶颈。

具体而言，现有工作的缺口体现在两个层面。其一，语音到表情的驱动机制主要依赖隐式情感特征或直接扩散，缺乏对细粒度面部动作的显式建模能力。例如，**EmoTalk3D**（Peng et al., ICCV 2023）虽然实现了情感解耦的3D面部动画，但其情感到表情的映射仍然是模糊的，难以通过外部信号进行精确控制。**Hallo3**等文本提示驱动的扩散方法虽然引入了编辑接口，但其编辑粒度较粗，难以实现对面部动作单元的精细化操控。其二，情感编辑接口的缺失或受限。**EAMM**（Ji et al., SIGGRAPH 2022）需要参考图像来驱动情感表达，**SadTalker**（Zhang et al., arXiv 2022）和**Real3D-Portrait**（Ye et al., arXiv 2024）则主要关注音频驱动的动画生成，缺乏对文本情感编辑的直接支持。

上述不足的根源在于：现有方法未能建立一个**可解释的中间表示**来桥接情感语义与面部动作。情感本质上是对特定面部动作单元（Action Unit, AU）的组合激活，而AU作为面部肌肉运动的解剖学编码，天然具备细粒度、可解释和可编辑的特性。然而，现有工作要么完全绕过AU空间进行端到端学习，要么仅在有限范围内使用AU信息，未能充分发挥其作为统一控制信号的潜力。

EmoDiffTalk的核心动机正是填补这一空白：**将AU代码空间作为情感感知的核心表示**，使其同时服务于两个关键功能——作为语音到表情的稀疏控制信号，以及作为文本到表情的编辑接口。这一设计使得模型既能从音频中精确推断面部动作，又能通过简单的文本指令实现对特定AU的增强或抑制，从而实现细粒度、解耦的情感动画生成。

## 核心创新

EmoDiffTalk 的核心创新在于引入**动作单元（Action Unit, AU）代码空间**作为情感与表情之间的可解释中间表示，并以此为基础构建了一套统一的情感感知高斯扩散框架，同时解决了“语音到表情的精细驱动”和“文本到表情的细粒度编辑”两个关键问题。

### 瓶颈突破：从隐式情感到显式AU映射

现有3D说话人头方法在情感建模上存在一个根本性瓶颈：情感到表情的映射是模糊且隐式的。无论是基于隐式情感特征（如 **EmoTalk3D**，Peng et al., ICCV 2023）还是直接对表情参数进行扩散（如 **Hallo3**），都难以通过文字或语音精确控制细粒度面部动作。EmoDiffTalk 的因果操纵变量在于：**显式建模AU代码空间**，将情感表达解耦为一组可解释的面部动作单元激活信号。这一设计使得情感不再是难以捉摸的隐变量，而是可量化、可编辑的稀疏控制信号。

### 三大关键 Changed Slots

相较于基线方法，EmoDiffTalk 在三个关键模块上实现了根本性替换：

| 技术槽位 | 基线方案 | EmoDiffTalk 方案 | 创新本质 |
|---------|---------|-----------------|---------|
| **颜色外观获取** | 球谐函数（SH） | 三重平面特征网格 + MLP解码 | 用可学习的显式特征网格替代固定基函数，提升高频细节的表达能力 |
| **语音到表情驱动** | 隐式情感特征或直接扩散 | AU代码作为扩散提示条件 | 将语音信号映射到可解释的AU空间，再以AU代码为条件引导高斯扩散过程 |
| **情感编辑接口** | 无直接编辑或需参考图像 | 文本映射到AU激活向量，增强-抑制变换 | 首次实现文本驱动的细粒度情感编辑，无需参考图像 |

### 颜色外观获取：从球谐函数到三重平面

传统3DGS使用球谐函数（SH）系数编码视角相关的颜色信息，但SH的表达能力受限于基函数阶数。EmoDiffTalk 在规范高斯Rig重建阶段（Sec. 3.1）替换为**三重平面特征网格**：对于空间中的每个点 $(x, y, z)$，从三个正交平面 $F_{xy}$、$F_{xz}$、$F_{yz}$ 上采样特征向量，拼接后经MLP解码得到颜色：

$$c = \mathcal{M}(F_{xy}(x, y) \oplus F_{xz}(x, z) \oplus F_{yz}(y, z))$$

这一设计将颜色信息显式存储在可学习的空间特征网格中，相比SH系数具备更强的局部细节建模能力，为后续精细的面部动画提供了更高质量的外观基础。

### 语音到表情驱动：AU提示高斯扩散

这是EmoDiffTalk最核心的机制创新。传统方法将语音特征直接映射到表情参数或顶点偏移，缺乏中间语义层的约束。EmoDiffTalk 引入了一个三阶段的**AU提示高斯扩散**流程（Sec. 3.2）：

1. **语音到AU编码器**：Transformer编码器将HuBERT音频特征序列 $\mathbf{A}_{0:T-1}$ 映射为连续的AU代码序列 $\mathcal{E}_{0:T-1}$：
   $$\mathcal{E}_{0:T-1} = \operatorname{Enc}(\mathbf{A}_{0:T-1}; \theta)$$

2. **AU提示高斯扩散**：扩散模型以AU代码 $\mathcal{E}_{0:T}$、网格模板 $\mathbf{P}$ 和音频特征 $\mathbf{A}_{0:T}$ 为联合条件，对网格顶点偏移进行去噪，预测动态高斯位置：
   $$\hat{\mathbf{x}}_{0:T}^{0} = D_{\theta}(\mathbf{x}_{0:T}^{n}, \mathbf{P}, \mathcal{E}_{0:T}, \mathbf{A}_{0:T}, n)$$

3. **动态外观解码器**：RotNet根据规范旋转、当前AU代码和变形位置预测高斯旋转；OPCNet利用可学习特征线和AU信息预测不透明度变化。

AU代码在这里充当了**稀疏语义锚点**的角色——它不是直接决定最终表情，而是作为扩散过程的提示条件，约束生成结果在解剖学上合理的表情空间内。消融实验（Table 3）有力验证了这一设计的必要性：移除AU代码对位置预测模块（w/o Codes4P）导致PSNR从25.78骤降至20.12；移除对不透明度预测的AU条件（w/o Codes4O）也使PSNR降至22.43。

### 情感编辑接口：文本到AU增强-抑制控制器

现有方法的情感编辑通常需要参考图像（如 **EAMM**，Ji et al., SIGGRAPH 2022）或缺乏直接编辑能力。EmoDiffTalk 首次实现了**纯文本驱动的细粒度情感编辑**（Sec. 3.3），其核心是一个文本到AU情感控制器：

- 将文本情感提示（如“开心地笑”）映射为二值AU激活向量 $\mathbf{y}$，指示哪些AU应被激活
- 通过增强-抑制变换调制原始AU代码：
  $$\tilde{\mathbf{E}}_{t} = \mathbf{E}_{t} \odot (1 + \alpha \mathbf{y}) - \beta (1 - \mathbf{y}) \odot \mathbf{E}_{t}$$
- 被激活的AU（$y_k=1$）以因子 $1+\alpha$ 增强，未激活的AU（$y_k=0$）以因子 $1-\beta$ 抑制

这一设计的精妙之处在于：它复用了语音驱动阶段训练好的AU代码空间和扩散模型，编辑操作仅需在AU层面进行简单的代数变换，无需重新训练扩散模型。用户研究（Table 2）证实，该方法在视频真实感和情感控制上均超过Hallo3，验证了AU空间作为编辑接口的有效性。

## 整体框架

EmoDiffTalk 的整体管道由两大阶段构成：**规范高斯Rig重建** 与 **情感感知高斯扩散**。前者从多视角图像中构建可驱动的基础三维高斯表示，后者以语音和文本情感提示为输入，驱动该表示生成动态的、可自由视角渲染的情感说话人头。

### 管道总览

如图 Figure 2 所示，系统首先对目标人物进行多视角图像采集，重建出带有变形绑定的规范高斯Rig。这一基础表示包含三重平面颜色预测网络，用于替代传统球谐函数(SH)以获取更优的颜色外观。随后，管道进入情感感知高斯扩散阶段，该阶段由三个核心模块串联构成：

![[assets/figures/papers/paper_list_l2474_https_openaccess_thecvf_com_content_CVPR2026_html_Liu_EmoDiffTalk_Emotio/figures/002_Figure_2.jpg]]
*Figure 2: Overall Pipeline of EmoDiffTalk. We first reconstruct the canonical Gaussian rig from a subject’s multi-view images, and then perform an emotion-aware Gaussian diffusion, including a AU-prompt Gaussian Diffusion process and Text-to-AU Emotion Controller, to animate the canonical Gaussian rig with any speech and text-based emotion prompt input, ultimately enabling free-viewpoint rendering via the 3DGS splatting*

1. **语音到AU编码器 (Speech-to-AU Encoder)**：将原始语音的HuBERT特征序列映射为连续的AU代码序列 $\pmb{\mathcal{E}}_{0:T-1}$，作为面部动作的稀疏、可解释控制信号。
2. **AU提示高斯扩散 (AU-prompt Gaussian Diffusion)**：以AU代码为条件，对网格顶点偏移进行去噪，预测动态高斯位置；同时，动态外观解码器（RotNet与OPCNet）根据AU代码和变形位置分别推理高斯的旋转与不透明度。
3. **文本到AU情感控制器 (Text-to-AU Emotion Controller)**：将文本情感提示映射为二值AU激活向量，通过增强-抑制机制调制AU代码，实现细粒度、解耦的情感编辑。

### 输入输出流

系统的输入分为两类驱动信号：
- **语音驱动**：原始音频经HuBERT编码后，由语音到AU编码器生成AU代码，再经扩散过程与外观解码器输出动态高斯属性。
- **文本情感驱动**：用户输入情感文本提示，文本到AU控制器将其转换为AU激活向量，对语音生成的AU代码进行调制，最终影响扩散与外观推理过程。

输出为任意视角下的三维高斯泼溅渲染结果，支持自由视点的高保真情感说话人头视频生成。

### 模块协同机制

管道中的关键设计在于AU代码作为统一的中间表示桥梁。它既是语音到表情的稀疏控制信号，又是文本到表情的编辑接口。这种设计使得语音驱动与情感编辑在同一个AU空间内解耦运作：语音提供时序动态基础，文本情感通过增强-抑制变换（见公式 $\tilde{\mathbf{E}}_t = \mathbf{E}_t \odot (1 + \alpha \mathbf{y}) - \beta (1 - \mathbf{y}) \odot \mathbf{E}_t$）对AU代码进行逐维调制，从而在不破坏唇同步的前提下注入情感表达。动态外观解码器中的OPCNet进一步利用可学习的特征线和AU信息预测不透明度变化，确保情感编辑在视觉细节层面的一致性。

### 训练策略

模型采用四阶段渐进训练策略：第一阶段训练语音到AU编码器；第二阶段训练AU提示高斯扩散；第三阶段训练动态外观解码器；第四阶段训练文本到AU情感控制器。各阶段逐步收敛，最终在单个NVIDIA RTX 5090 GPU上约需3天完成全部训练。

## 核心模块与公式推导

### 3.1 规范高斯Rig重建与三重平面颜色表示

EmoDiffTalk首先从多视角图像重建一个绑定变形场的规范3D高斯Rig。与常见的球谐函数(SH)颜色表示不同，该方法采用**三重平面特征网格**来获取颜色外观，以提升颜色属性分配的精度。对于规范空间中的每一个点 $(x, y, z)$，其颜色 $c$ 由三个正交平面特征图拼接后经MLP解码得到：

$$c = \mathcal{M}(F_{xy}(x,y) \oplus F_{xz}(x,z) \oplus F_{yz}(y,z))$$

其中 $F_{xy}$、$F_{xz}$、$F_{yz}$ 分别表示 $xy$、$xz$、$yz$ 三个平面的可学习特征图，$\oplus$ 表示特征拼接操作，$\mathcal{M}$ 为一个轻量MLP解码器。这一设计使得颜色预测能够从多视角信息中更鲁棒地提取外观特征，为后续的动态外观推理奠定基础。

### 3.2 语音到AU编码器

情感感知高斯扩散的核心在于将语音信号映射为可解释的动作单元(Action Unit, AU)代码。给定一段原始音频，首先通过预训练的HuBERT提取自监督特征序列：

$$\pmb{A}_{0:T-1} = \{\pmb{A}_t \mid t=0,\ldots,T-1\}, \quad \pmb{A}_t \in \mathbb{R}^{768}$$

随后，一个Transformer编码器将该特征序列映射为连续的AU代码序列：

$$\pmb{\mathcal{E}}_{0:T-1} = \operatorname{Enc}(\pmb{A}_{0:T-1}; \theta)$$

其中 $\pmb{\mathcal{E}}_{0:T-1}$ 为预测的AU代码序列，$\theta$ 为编码器参数。这些AU代码作为稀疏且可解释的面部动作控制信号，既充当后续扩散过程的条件提示，又为情感编辑提供统一的接口空间。

### 3.3 AU提示高斯扩散

AU提示高斯扩散过程以AU代码为核心条件，对网格顶点偏移进行去噪，从而生成动态的高斯位置序列。具体而言，扩散模型 $D_{\theta}$ 接收噪声化的位置序列 $\pmb{x}_{0:T}^{n}$、网格模板 $\pmb{P}$、AU代码序列 $\pmb{E}_{0:T}$ 以及音频特征 $\pmb{A}_{0:T}$，预测去噪后的位置序列：

$$\hat{\pmb{x}}_{0:T}^{0} = D_{\theta}(\pmb{x}_{0:T}^{n}, \pmb{P}, \pmb{E}_{0:T}, \pmb{A}_{0:T}, n)$$

其中 $n$ 为当前噪声步数。与直接回归相比，扩散策略能够更好地捕捉面部运动的复杂分布，生成更自然、细腻的动态表情。

### 3.4 动态外观解码器

在获得动态位置后，EmoDiffTalk通过两个专用网络分别解码高斯的旋转和不透明度属性。**旋转预测网络(RotNet)** 根据规范旋转 $R_0$、当前AU代码 $E_t$ 和变形位置 $\mu_t$ 预测逐帧的高斯旋转：

$$R_t = \mathcal{N}_{\mathrm{Rot}}(R_0, E_t, \mu_t)$$

**不透明度预测网络(OPCNet)** 则利用可学习的特征线和AU信息预测不透明度变化，以捕捉面部表情变化中如皱纹、阴影等细微的外观细节。两个网络均以AU代码为条件输入，确保外观变化与面部动作语义一致。

### 3.5 文本到AU情感控制器

为实现文本驱动的情感编辑，EmoDiffTalk设计了文本到AU情感控制器。该模块首先将文本情感提示映射为二值AU激活向量 $\mathbf{y}$，随后通过增强-抑制机制对原始AU代码进行调制：

$$\tilde{\mathbf{E}}_t = \mathbf{E}_t \odot (1 + \alpha \mathbf{y}) - \beta (1 - \mathbf{y}) \odot \mathbf{E}_t$$

其中 $\alpha$ 和 $\beta$ 分别为增强和抑制系数，$\odot$ 表示逐元素乘法。当某个AU被激活($y_k=1$)时，其代码值被放大 $1+\alpha$ 倍；当未被激活($y_k=0$)时，其代码值被衰减 $1-\beta$ 倍。调制后的情感AU代码 $\tilde{\mathbf{E}}_{0:T-1}$ 替换原始AU代码作为扩散过程的条件输入，从而驱动相应的情感表达。该机制使得用户可以通过简单的文本描述（如“开心地笑”）精确控制面部动作的细粒度情感表现。

### 补充图表

![[assets/figures/papers/paper_list_l2474_https_openaccess_thecvf_com_content_CVPR2026_html_Liu_EmoDiffTalk_Emotio/figures/003_Figure_3.jpg]]
*Figure 3: Text-to-AU Emotion Controller pipeline (left) and AUbased emotion editing for Gaussian appearance inference (right)*

## 实验与分析

### 定量评估与对比

EmoDiffTalk 在两个主流数据集上进行了全面的定量评估：**EmoTalk3D**（情感解耦的3D面部动画数据集）和 **RenderMe-360**（多视角动态人像数据集）。评估指标涵盖像素级重建质量（PSNR、SSIM）、感知相似度（LPIPS）、唇动同步度（LMD）以及感知模糊度（CPBD）。

**Table 1** 展示了完整的定量对比结果。在 EmoTalk3D 数据集上，EmoDiffTalk 取得了 **PSNR 25.78** 的显著成绩，相较于其基础框架 **EmoTalk3D**（Peng et al., ICCV 2023）的 21.22 提升了 **+4.56 dB**，表明在像素级重建精度上有质的飞跃。在感知清晰度指标 CPBD 上，EmoDiffTalk 达到 **0.36**，超过 **Hallo3** 基线 0.31 约 **+16.1%**，说明生成的图像边缘和细节更加锐利。同时，EmoDiffTalk 的 LPIPS 为 **0.12**，在所有对比方法中达到最优，验证了其生成结果在感知层面与真实视频的高度一致性。在唇动同步度 LMD 上，EmoDiffTalk 取得 **3.56** 的最低值，显著优于其他方法，证明了 AU 代码空间对语音到表情映射的精确建模能力。

在 RenderMe-360 数据集上的跨数据集泛化评估进一步验证了方法的鲁棒性。EmoDiffTalk 的 LMD 为 **6.59**，相较于 Hallo3 的约 9.34 降低了 **29.4%**，PSNR 达到 **21.41**（Hallo3 约 20.13），在保持唇同步优势的同时实现了更好的重建质量。值得注意的是，RenderMe-360 包含更丰富的头部姿态和光照变化，EmoDiffTalk 在该数据集上的稳定表现说明其动态外观解码器（RotNet 与 OPCNet）对不同场景具有良好的适应能力。

**Figure 4** 和 **Figure 5** 提供了定性视觉对比。在 EmoTalk3D 数据集上，EmoDiffTalk 在唇形准确度和面部纹理细节（如皱纹、牙齿边缘）上均明显优于包括 Real3D-Portrait、EchoMimic 在内的现有方法。Hallo3 等方法在唇部区域常出现模糊或错位，而 EmoDiffTalk 的 AU 提示扩散过程能够生成更精确的顶点偏移，从而驱动更自然的唇动和表情变化。

### 用户研究

为评估主观感知质量，研究团队进行了用户研究（**Table 2**），邀请参与者对音视频同步、视频保真度、图像质量和情感控制四个维度进行评分。在 EmoTalk3D 数据集上，EmoDiffTalk 的视频保真度超过 Hallo3 **+5.3%**，图像质量超过 **+4.7%**；在 RenderMe-360 数据集上，视频保真度超过 **+1.7%**，情感控制超过 **+2.2%**。情感控制维度的优势直接验证了文本到 AU 情感控制器作为编辑接口的有效性——用户能够感知到文本提示所对应的情感在生成视频中的准确表达。

![[assets/figures/papers/paper_list_l2474_https_openaccess_thecvf_com_content_CVPR2026_html_Liu_EmoDiffTalk_Emotio/figures/007_Table_2.jpg]]
*Table 2: The quantitative comparison of talking head generation quality user study using different comparing approaches respectively*

### 消融实验

为验证各核心模块的贡献，论文设计了系统的消融实验（**Table 3** 和 **Figure 6**），考察三个关键变体：

![[assets/figures/papers/paper_list_l2474_https_openaccess_thecvf_com_content_CVPR2026_html_Liu_EmoDiffTalk_Emotio/figures/008_Figure_6.jpg]]
*Figure 6: Visual results of Ablation Study for the key modules within different system variants including ’w/o Codes4P’, ’w/o Codes4O’, ’w/o Diffusion’ and our ’FULL’ respectively*

![[assets/figures/papers/paper_list_l2474_https_openaccess_thecvf_com_content_CVPR2026_html_Liu_EmoDiffTalk_Emotio/figures/009_Table_3.jpg]]
*Table 3: Quantitative Comparison of Ablation Study for the key modules within different system variants including ’w/o Codes4P’, ’w/o Codes4O’, ’w/o Diffusion’ and our ’FULL’ respectively*

- **w/o Codes4P**：移除 AU 代码对位置预测模块的输入。该变体 PSNR 骤降至 **20.12**，相比完整模型的 25.78 下降超过 5 dB。这表明 AU 代码作为扩散条件对于定位高斯顶点的动态偏移至关重要——缺少 AU 引导时，扩散过程无法准确预测面部区域的精细运动，导致唇形和表情严重失真。

- **w/o Codes4O**：移除 AU 代码对不透明度预测模块（OPCNet）的输入。PSNR 降为 **22.43**，降幅虽小于 Codes4P，但仍显著。这验证了 AU 信息在表现面部细节（如皱纹随表情的显现与消失、嘴唇边缘的透明度变化）中的关键作用。OPCNet 利用可学习的特征线和 AU 信息预测不透明度变化，缺少该条件会导致细节模糊。

- **w/o Diffusion**：用简单的 GRU 网络替代扩散过程。PSNR 为 **24.96**，虽仍可接受，但相比完整模型仍有明显差距。这证明了扩散策略在捕捉运动分布多模态性方面的优势——面部运动具有高度的非确定性和多样性，扩散模型能够更好地建模这种复杂分布，而确定性回归网络倾向于生成平均化的运动轨迹，导致表情僵硬。

完整模型（FULL）在所有指标上取得最优，证实了 AU 提示扩散、动态外观解码器以及位置/不透明度双路 AU 条件注入的协同贡献。**Figure 6** 的视觉结果与定量指标一致：w/o Codes4P 导致唇部区域严重错位，w/o Codes4O 使面部细节（如牙齿、皱纹）模糊，w/o Diffusion 则使整体表情显得僵硬不自然。

### 失败模式与局限性

尽管 EmoDiffTalk 在定量和定性评估中表现优异，论文明确指出了两个主要局限：

1. **计算开销**：当前框架依赖于多个预训练网络（HuBERT 音频编码器、扩散去噪网络、三重平面特征网格等），训练需在单张 NVIDIA RTX 5090 GPU（32GB）上耗时约 3 天，限制了实时应用部署。如何压缩模型规模、降低推理延迟是未来工作的重要方向。

2. **极端表情编辑失效**：文本到 AU 的增强-抑制控制器在面对超出训练分布的极端夸张表情时可能失效。该控制器通过二值 AU 激活向量和增强/抑制系数调制 AU 代码，当目标表情涉及训练数据中罕见的 AU 组合或极端激活强度时，线性调制策略可能无法准确生成对应的面部动作，导致编辑不准确。

此外，AU 代码空间作为中间表示的泛化边界尚未被充分探索——能否联合语音情感等其他模态实现更自然的混合编辑，以及如何设计更鲁棒的 AU 调制策略来应对分布外表情，仍是值得研究的开放问题。

### 补充图表

![[assets/figures/papers/paper_list_l2474_https_openaccess_thecvf_com_content_CVPR2026_html_Liu_EmoDiffTalk_Emotio/figures/004_Table_1.jpg]]
*Table 1: Quantitative comparison results evaluated on the Emotalk3D and RenderMe-360 datasets using different comparing approaches respectively*

![[assets/figures/papers/paper_list_l2474_https_openaccess_thecvf_com_content_CVPR2026_html_Liu_EmoDiffTalk_Emotio/figures/005_Figure_4.jpg]]
*Figure 4: Qualitative Comparison on the Emotalk3D Dataset. Our approach outperforms existing approaches in both lip-sync accuracy and facial reconstruction detail than those previous SOTA talking head approaches*

![[assets/figures/papers/paper_list_l2474_https_openaccess_thecvf_com_content_CVPR2026_html_Liu_EmoDiffTalk_Emotio/figures/006_Figure_5.jpg]]
*Figure 5: Additional experimental results on the Emotalk3D dataset and comparative evaluation results on the RenderMe-360 benchmark*

![[assets/figures/papers/paper_list_l2474_https_openaccess_thecvf_com_content_CVPR2026_html_Liu_EmoDiffTalk_Emotio/figures/001_Figure_1.jpg]]
*Figure 1: Text-to-AU based emotion editing results of our EmoDiffTalk. Our EmoDiffTalk not only supports fine-grained speechdriven (third row) 3DGS talking head generation (first row), but also enabling expansive and accurate text-based emotion editing (second and fourth rows). The AU Code (bottom) are also demonstrated. Please refer to our demo video for more text driven 3D talking head editing results*

## 方法谱系与知识库定位

### 1. 与基线工作的关系

EmoDiffTalk 的核心贡献在于将**动作单元（Action Unit, AU）代码空间**显式引入3D高斯说话人头动画管道，以替代此前方法中模糊的隐式情感特征映射。其方法定位可以从以下几条谱系线梳理：

- **情感驱动的2D/3D说话人脸线**：早期工作如 **EAMM**（Ji et al., SIGGRAPH 2022）通过参考图像实现情感编辑，**SadTalker**（Zhang et al., arXiv 2022）则利用音频驱动3D面部动画。这些方法或依赖参考图像、或在情感控制粒度上受限。EmoDiffTalk 的文本到AU控制器提供了一条无需参考图像、直接由自然语言描述驱动细粒度情感编辑的新路径。

- **3D对话人像合成线**：**Real3D-Portrait**（Ye et al., arXiv 2024）和 **Hallo3** 代表了基于扩散模型的3D头像生成前沿。Hallo3 采用文本提示直接驱动音频扩散生成，但在情感控制精度和可编辑性上存在局限——EmoDiffTalk 在 EmoTalk3D 数据集上将 CPBD 指标提升 16.1%，并在用户研究的情感控制维度上超过 Hallo3，验证了 AU 中间表示相较于直接文本条件注入的优势。

- **情感解耦3D面部动画线**：**EmoTalk3D**（Peng et al., ICCV 2023）是本文所采用框架的基础，其贡献在于情感解耦的面部动画建模。EmoDiffTalk 在此基础上做了两个关键替换：(1) 将隐式情感特征替换为显式 AU 代码作为条件信号；(2) 将确定性解码替换为 AU 提示的高斯扩散过程。定量结果显示，在 EmoTalk3D 数据集上 PSNR 提升 4.56 dB，LPIPS 降至 0.12，表明 AU 代码空间与扩散策略的协同作用显著优于原框架。

- **视频扩散驱动动态肖像线**：**EchoMimic** 等视频扩散方法在2D动态肖像生成上表现突出，但其3D一致性受限。EmoDiffTalk 在3DGS框架内引入扩散过程，既保留了扩散模型对运动分布建模的优势，又通过显式3D表示保证多视角一致性。

### 2. 核心机制差异：AU代码作为因果调节变量

EmoDiffTalk 的因果调节变量是 **AU 代码空间**，它在管道中扮演双重角色：

1. **语音到表情的稀疏控制信号**：语音到AU编码器（Speech-to-AU Encoder）将 HuBERT 音频特征映射为连续的 AU 代码序列，该序列作为条件注入高斯扩散过程，驱动网格顶点偏移的预测。消融实验表明，移除 AU 代码对位置预测模块（w/o Codes4P）导致 PSNR 从 25.78 骤降至 20.12，证实 AU 条件对精细动态定位的因果性作用。

2. **文本到表情的编辑接口**：文本到AU情感控制器将自然语言情感提示映射为二值 AU 激活向量，通过增强-抑制变换（式7）调制原始 AU 代码，实现解耦的情感编辑。这一设计的独特之处在于：AU 空间天然具备解剖学可解释性，使得编辑操作（增强/抑制特定 AU）与面部肌肉运动之间存在直接对应关系，避免了端到端黑箱编辑的不确定性。

### 3. 技术槽位替换与适用边界

**已变更的技术槽位**包括：

- **颜色外观获取**：从球谐函数（SH）替换为三重平面特征网格与MLP解码（式1），提升了颜色属性的表达能力。
- **语音到表情驱动**：从隐式情感特征或直接扩散替换为基于 AU 代码的高斯扩散，AU 代码作为扩散提示条件（式4）。
- **情感编辑接口**：从无直接编辑或需要参考图像替换为文本映射到 AU 激活向量的增强-抑制调制（式7）。

**适用边界**：

- 当前框架依赖于多个预训练网络（HuBERT、AU检测器等），带来显著计算开销（单卡 RTX 5090 训练约3天），限制了实时应用场景。
- 文本到AU增强-抑制控制器在面对极端夸张表情时可能失效——增强/抑制系数的线性调制策略难以覆盖超出训练分布的非线性表情变化。
- AU 代码空间的表达能力受限于预定义的动作单元集合，对于文化特异性或个体化的微表情可能缺乏对应的 AU 编码。

### 4. 开放问题

1. **模型压缩与实时化**：如何压缩预训练组件规模或通过知识蒸馏降低推理延迟，是走向实时应用的关键。
2. **鲁棒的情感调制策略**：能否设计非线性的、条件自适应的 AU 调制机制（如基于扩散的 AU 编辑或学习式变换），以处理超出训练分布的极端表情？
3. **多模态联合编辑**：AU 代码空间能否联合语音情感特征、面部动作捕捉等其他模态，实现更自然的混合情感编辑（如语音悲伤+文本愤怒的冲突情感合成）？
4. **跨身份泛化**：当前方法需要为每个说话人重建规范高斯Rig，能否通过元学习或条件生成实现少样本甚至零样本的身份泛化？

## 原文 PDF

![[paperPDFs/CVPR_2026/EmoDiffTalk_Emotion_aware_Diffusion_for_Editable_3D_Gaussian_Talking_Head.pdf]]
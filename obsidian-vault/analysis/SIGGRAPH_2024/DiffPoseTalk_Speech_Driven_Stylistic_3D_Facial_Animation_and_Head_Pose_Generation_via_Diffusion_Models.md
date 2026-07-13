---
title: "DiffPoseTalk: Speech-Driven Stylistic 3D Facial Animation and Head Pose Generation via Diffusion Models"
type: paper
paper_level: A
venue: SIGGRAPH
year: 2024
pdf_ref: paperPDFs/SIGGRAPH_2024/DiffPoseTalk_Speech_Driven_Stylistic_3D_Facial_Animation_and_Head_Pose_Generation_via_Diffusion_Models.pdf
project_link: https://diffposetalk.github.io
code_link: null
aliases:
- DiffPoseTalk
tags:
- SIGGRAPH_2024
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 扩散概率模型的反向去噪过程与基于对比学习的说话风格编码器相结合，通过无分类器引导实现个性化和多样化的风格控制。
primary_logic: 利用扩散模型拟合语音、风格和面部动作的复杂联合分布，通过对比学习从参考视频中提取风格嵌入，在无需微调的情况下泛化到任意新风格，同时生成头部姿态以增强真实感。
claims:
- 采用扩散模型预测干净样本而非噪声，并添加几何损失以提供更精确的面部运动约束。
- 引入基于对比学习的说话风格编码器，能够从任意参考视频中提取风格嵌入，并通过无分类器引导控制生成。
- 在TFHP数据集上，DiffPoseTalk在LVE、FDD、MOD、BA等指标上全面超越现有最佳方法。
- 消融实验证实风格编码器、几何损失、对齐掩码和无分类器引导对最终性能至关重要。
---

# DiffPoseTalk: Speech-Driven Stylistic 3D Facial Animation and Head Pose Generation via Diffusion Models

> [!tip] 核心洞察
> 利用扩散模型拟合语音、风格和面部动作的复杂联合分布，通过对比学习从参考视频中提取风格嵌入，在无需微调的情况下泛化到任意新风格，同时生成头部姿态以增强真实感。

| 字段 | 内容 |
|------|------|
| 中文题名 | DiffPoseTalk：基于扩散模型的语音驱动风格化3D面部动画与头部姿态生成 |
| 英文题名 | DiffPoseTalk: Speech-Driven Stylistic 3D Facial Animation and Head Pose Generation via Diffusion Models |
| 会议/期刊 | SIGGRAPH 2024 |
| Links | [Project](https://diffposetalk.github.io) · [paper](http://arxiv.org/abs/1412.6980) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | DiffPoseTalk |
| Dataset | TFHP |

> [!tip] 效果简介
> - TFHP (测试集) 上，LVE (Lip Vertex Error) 8.94 vs FaceDiffuser (显著优于所有对比方法 (越低越好))；FDD (Facial Dynamics Deviation) 9.60 vs FaceDiffuser (显著优于所有对比方法 (越低越好))；MOD (Mouth Opening Deviation) 1.62 vs FaceDiffuser (显著优于所有对比方法 (越低越好))。

## 概要

语音驱动的3D面部动画在虚拟化身、游戏和影视制作中需求广泛，但该任务面临一个本质性瓶颈：**语音到面部动作存在天然的多对多映射**——同一段语音可以对应多种合理的面部表情和头部运动。现有方法多采用确定性回归模型（如**FaceFormer**，Fan et al., CVPR 2022），将语音直接映射为单一的面部动作序列，导致生成结果过度平滑、缺乏表现力，且丧失了动作的多样性与个性化风格。此外，基于one-hot编码的风格控制方式（如**CodeTalker**，Xing et al., CVPR 2023）缺乏泛化能力，难以适应训练集中未出现的新说话风格。

针对上述问题，**DiffPoseTalk** 提出了一套基于扩散概率模型的生成框架，核心思想是：利用扩散模型拟合语音、风格与面部动作之间的复杂联合分布，通过反向去噪过程从噪声中逐步恢复出多样化且风格可控的3D面部动画与头部姿态。该方法的关键创新包括三个层面：

1. **扩散生成替代确定性映射**：采用Transformer去噪网络直接预测干净的运动参数（而非标准扩散模型中的噪声），使得可以在训练中引入顶点损失、速度损失和平滑损失等几何约束，从而在保持生成多样性的同时确保面部动画的精确性。
2. **对比学习驱动的风格编码器**：设计了一个基于Transformer的说话风格编码器，通过NT-Xent对比损失从任意参考视频的运动参数序列中提取身份无关的风格嵌入。该编码器无需针对新风格进行微调，即可泛化到训练集以外的任意说话风格。
3. **无分类器引导的灵活控制**：在推理阶段采用增量式无分类器引导，通过独立的语音引导权重 $w_a$ 和风格引导权重 $w_s$，分别调节生成结果对语音内容和目标风格的遵从程度，实现个性化和多样化的风格控制。

在TFHP数据集上的定量评估显示，DiffPoseTalk在唇部顶点误差（LVE: 8.94）、面部动态偏差（FDD: 9.60）、张嘴幅度偏差（MOD: 1.62）和头部姿态节拍对齐（BA: 0.29）等指标上全面超越现有最佳方法**FaceDiffuser**（Stan et al., MIG 2023）及其他基线。消融实验进一步证实，风格编码器的移除会导致所有指标下降，几何损失的去除使模型无法生成精确的面部动画，而对齐掩码的缺失则引发严重的音画不同步问题。用户研究（31名参与者）也表明，DiffPoseTalk在口型同步、风格相似度和自然度上均获得了最高的盲评偏好。

**方法定位**：DiffPoseTalk属于扩散生成式语音驱动面部动画方法，在生成范式上区别于确定性回归方法（FaceFormer、CodeTalker）和基于示例的个性化方法（**Imitator**，Thambiraja et al., ICCV 2023；**SadTalker**，Zhang et al., CVPR 2023），在风格控制机制上区别于基于one-hot编码的方案。其扩散预测干净样本、对比风格编码与无分类器引导的组合设计，为语音驱动动画领域提供了一种兼顾多样性、精确性和泛化能力的技术路线。

语音驱动的3D面部动画旨在从语音信号中生成与音频同步的面部表情和头部运动，在虚拟人、游戏和影视制作中有广泛应用。这一任务的核心难点在于**语音到面部动作的映射具有内在的多对多特性**——同一段语音可以对应多种合理的面部表情和头部姿态，取决于说话者的个人风格、情绪状态和语境。

现有方法大多采用确定性回归模型来解决这一问题。例如，**FaceFormer**（Fan et al., CVPR 2022）使用基于Transformer的自回归架构直接从语音特征映射到面部运动参数；**CodeTalker**（Xing et al., CVPR 2023）引入离散动作先验来约束生成空间。这些确定性方法虽然能够产生基本同步的唇部动作，但面临两个根本性瓶颈：

**瓶颈一：动作过度平滑与均值回归。** 确定性模型倾向于学习语音到动作的一对一映射，输出的是条件分布的均值。这导致生成的面部动画缺乏表现力，动作幅度偏小，难以捕捉真实说话中丰富的微表情和节奏变化。本质上，这类模型无法建模语音与面部动作之间复杂的多模态联合分布。

**瓶颈二：风格编码缺乏泛化能力。** 现有风格化方法通常依赖one-hot身份编码或固定的风格标签，如**Imitator**（Thambiraja et al., ICCV 2023）和**EmoTalk**（Peng et al., ICCV 2023）。这种设计使得模型只能处理训练集中见过的说话风格，无法泛化到任意新的说话者。要从参考视频中提取并迁移未见过的个性化说话风格，需要一种更灵活的风格表示机制。

此外，头部姿态生成在现有工作中常被忽视或单独处理。**SadTalker**（Zhang et al., CVPR 2023）和**FaceDiffuser**（Stan et al., MIG 2023）虽然引入了扩散模型来增强多样性，但在风格解耦和头部姿态与语音节奏的对齐方面仍有不足。**MeshTalk**（Richard et al., ICCV 2021）尝试通过交叉模态解耦来实现面部动画，但同样受限于确定性架构的表达能力。

针对上述问题，**DiffPoseTalk**提出了一种基于扩散概率模型的新范式。其核心动机在于：扩散模型天然适合拟合复杂的多模态分布，能够从同一语音条件中采样出多样化且合理的面部动作；同时，通过引入基于对比学习的说话风格编码器和无分类器引导机制，模型可以从任意参考视频中提取风格嵌入，在无需微调的情况下实现个性化和多样化的风格控制。联合生成头部姿态进一步增强了动画的真实感和节奏对齐。

## 核心方法与创新机理

DiffPoseTalk 的核心创新在于通过**扩散概率模型**与**对比学习风格编码器**的协同设计，系统性地解决了语音驱动3D面部动画中的两个根本性瓶颈：确定性映射导致的动作过度平滑，以及固定风格标签无法泛化到新说话风格的局限。

### 从确定性映射到扩散生成

传统方法（如 **FaceFormer**，Fan et al., CVPR 2022）采用确定性回归模型，将语音特征直接映射为面部动作参数。这种一对一映射无法捕捉语音到面部动作的多对多关系，导致生成结果趋向均值、缺乏表现力。DiffPoseTalk 转而采用**扩散概率模型**来拟合语音、风格与面部动作之间的复杂联合分布，从根本上赋予了生成多样性和风格化能力。

在扩散模型的具体设计上，DiffPoseTalk 做出了关键改进：**去噪网络直接预测干净样本 $X^0$ 而非噪声**。这一选择使得可以在训练中直接施加几何约束，为面部运动提供更精确的监督信号。

### 从固定标签到可泛化风格编码

现有方法（如 **Imitator**，Thambiraja et al., ICCV 2023）通常使用 one-hot 身份编码或固定风格标签，无法适应训练集中未见过的说话风格。DiffPoseTalk 设计了**基于 Transformer 的说话风格编码器**，能够从任意参考视频的运动参数序列中提取风格嵌入 $s = SE(X_{0:T})$。该编码器通过 **NT-Xent 对比损失**进行训练，最大化同一说话人不同片段的风格相似度，最小化不同说话人的风格相似度，从而学习到身份无关的、可迁移的说话风格表征。推理时，用户只需提供一段参考视频，即可将任意新风格注入生成过程，无需任何微调。

### 无分类器引导的精细化条件控制

为了在生成过程中灵活平衡语音内容和风格表达的影响，DiffPoseTalk 引入了**增量式无分类器引导**机制。采样时通过两个独立的引导权重 $w_a$（语音引导）和 $w_s$（风格引导），分别控制模型对语音条件和风格条件的遵从程度：

$$\hat{X}^{0} = D(X^n,\emptyset,\emptyset,\beta,n) + w_a\left[D(X^n,A,\emptyset,\beta,n)-D(X^n,\emptyset,\emptyset,\beta,n)\right] + w_s\left[D(X^n,A,s,\beta,n)-D(X^n,A,\emptyset,\beta,n)\right]$$

这种解耦的引导策略使用户可以独立调节唇形同步精度和风格化强度，实现个性化的生成控制。

### 几何感知的扩散训练

DiffPoseTalk 在标准扩散损失 $\mathcal{L}_{\mathrm{simple}}$ 之上，额外引入了三个几何损失项，直接在3D网格顶点层面施加约束：

- **顶点损失** $\mathcal{L}_{\mathrm{vert}}$：约束预测网格与真实网格的顶点位置一致
- **速度损失** $\mathcal{L}_{\mathrm{vel}}$：保持相邻帧之间顶点运动的时序一致性
- **平滑损失** $\mathcal{L}_{\mathrm{smooth}}$：惩罚顶点加速度，抑制抖动

这些几何损失的加入使得扩散模型不仅学习数据分布，还能生成几何精度更高、时序更平滑的面部动画。消融实验证实，移除所有几何损失后，模型无法生成精确的面部动画。

### 时序对齐的结构化设计

DiffPoseTalk 在 Transformer 去噪网络的编码器-解码器之间引入了**对齐掩码**，确保每个运动时间步仅关注对应的语音帧，而非全局语音序列。这一设计与 FaceFormer 的对齐策略一脉相承，但在扩散生成框架下起到了关键的时序约束作用。消融实验表明，移除对齐掩码会导致严重的音画不同步问题。

### 头部姿态的联合生成

与大多数仅关注面部表情的方法不同，DiffPoseTalk 将**头部姿态生成**纳入统一的扩散框架，使模型能够同时预测表情参数和头部旋转/平移参数。这使得生成的动画在语音节奏与头部运动之间实现了自然的节拍对齐，在 BA 指标上取得了 0.29 的最佳成绩，显著超越了仅生成表情的对比方法。

DiffPoseTalk 的整体 pipeline 围绕扩散概率模型构建，核心思路是将语音驱动的面部动画生成建模为一个条件生成问题：给定输入语音和参考说话风格，生成多样化且风格一致的面部运动参数（包含表情、头部姿态）以及对应的 3D 面部网格。系统由五个关键模块串联而成，形成“语音编码—风格提取—条件去噪—网格重建—时序平滑”的完整推理链路。

### 输入与输出流

系统的输入包括：（1）一段任意长度的原始语音波形；（2）一个可选的参考风格视频片段，用于提取目标说话人的个性化风格；（3）目标说话人的身份形状参数 β，可通过单张图像由 MICA 等工具离线重建。输出为与语音同步的 3D 面部网格序列，包含唇部运动、面部表情和头部姿态。

### 模块关系与数据流

1. **HuBERT 语音编码器**：将原始语音波形转换为帧级语音特征。采用预训练的 HuBERT 模型，通过重采样层将特征帧率对齐到面部动画的目标帧率（25 FPS），得到语音特征序列 A。HuBERT 的 transformer 层在训练中可端到端微调，以更好地适应面部动画任务。

2. **说话风格编码器**：从参考视频的运动参数序列中提取身份无关的风格嵌入 s。该模块是一个四层 transformer 编码器（四个注意力头），将运动序列 X_{0:T} 映射为 128 维的风格向量。训练时采用对比学习策略（NT-Xent loss），使同一说话人的不同片段在嵌入空间中彼此靠近，不同说话人的片段相互远离，从而获得可泛化到任意新说话人的风格表示。

3. **Transformer 去噪网络**：这是系统的核心生成模块。采用八层 transformer 解码器（八个注意力头），接收含噪运动参数 X^n、前一时间窗的干净运动 X^0_{-T_p:0}、语音特征 A、风格嵌入 s、身份形状 β 和扩散时间步 n，预测干净的运动参数 X̂^0。与标准扩散模型预测噪声不同，DiffPoseTalk 直接预测干净样本，这使得可以在训练中直接施加几何损失（顶点损失、速度损失、平滑损失）以提供更精确的面部运动约束。为解决长序列生成问题，采用窗口策略：每次处理长度为 T_w 的时间窗，并保留前 T_p 帧作为上下文，通过滑动窗口覆盖任意长度的输入。

4. **无分类器引导采样器**：在推理阶段，通过增量式无分类器引导机制分别控制语音条件和风格条件对生成结果的影响强度。具体而言，采样公式为：
   $$\hat{X}^{0} = D(X^n,\emptyset,\emptyset,\beta,n) + w_a\left[D(X^n,A,\emptyset,\beta,n)-D(X^n,\emptyset,\emptyset,\beta,n)\right] + w_s\left[D(X^n,A,s,\beta,n)-D(X^n,A,\emptyset,\beta,n)\right]$$
   其中 w_a 和 w_s 分别调节语音同步性和风格个性化程度，通过调整这两个引导权重可在多样性和条件遵从度之间实现灵活权衡。

5. **3DMM 重建与平滑模块**：去噪网络输出的运动参数 x（包含 FLAME 模型的表情系数和下颌姿态）与身份形状 β 一起，通过 FLAME 3D 可变形模型重建为 3D 面部网格 M(β, x)。头部姿态参数则通过 6DRepNet 从原始视频中估计（训练时）或由去噪网络直接预测（推理时）。最终对重建的面部网格序列施加 Savitzky-Golay 滤波器以消除高频抖动，提升视觉平滑度。

### 训练与推理流程差异

训练时，所有条件（语音、风格、形状）均从真实数据中提取，去噪网络通过最小化预测干净样本与真实干净样本之间的 L_simple 损失以及顶点、速度、平滑度等几何损失来优化参数。推理时，语音和形状由用户提供，风格嵌入可从任意参考视频中一次性提取，然后通过迭代去噪过程（从纯噪声开始，逐步去噪直至生成干净运动参数）完成生成。无分类器引导仅在推理时启用，以增强对语音和风格条件的遵从度。

![[assets/figures/papers/paper_list_l1923_DiffPoseTalk_Speech_Driven_Stylistic_3D_Facial_Animation_and_Head_Pose_G/figures/001_Figure_1.jpg]]
*Figure 1: We present DiffPoseTalk, a novel diffusion-based speech-driven animation system incorporated with a speaking style encoder to extract style features from arbitrary reference videos. Given an input speech and a speaking style, our system generates diverse and stylistic facial animations along with head movements*

DiffPoseTalk 的核心架构由三个紧密协作的模块构成：语音编码器、Transformer 去噪网络和说话风格编码器，三者通过扩散模型的去噪框架和几何损失函数实现精确的面部动画生成。

### 3DMM 面部表示与语音编码

系统采用 FLAME 三维可变形模型作为面部表示。FLAME 的网格构建公式为：

$$M(\beta, \theta, \psi) = W(T_P(\beta, \theta, \psi), J(\beta), \theta, \mathcal{W})$$

其中 $\beta$ 为形状参数，$\theta$ 为姿态参数，$\psi$ 为表情参数。为简化表示，作者将表情参数和下颌姿态参数合并为运动参数 $x$，将网格构建重写为 $M(\beta, x)$。3DMM 参数通过 MICA（形状预测）、SPECTRE（唇部运动和下颌姿态）和 6DRepNet（头部旋转）联合重建，并经 Savitzky-Golay 滤波器平滑处理。

语音编码方面，采用 HuBERT 预训练模型提取帧级语音特征。为适应面部动画的帧率，在 HuBERT 的时间卷积层后引入重采样层，使语音特征与运动参数的时序对齐。

### Transformer 去噪网络与窗口策略

去噪网络是扩散模型反向过程的核心。与标准扩散模型预测噪声不同，DiffPoseTalk 直接预测干净样本 $X^0$，以便在训练中融入几何损失。去噪网络的基础输出为：

$$\hat{X}_{-T_p:T_w}^{0} = D\left( X_{0:T_w}^{n}, X_{-T_p:0}^{0}, A_{-T_p:T_w}, n \right)$$

其中 $X_{0:T_w}^{n}$ 为当前窗口的含噪运动参数，$X_{-T_p:0}^{0}$ 为先前窗口的干净运动参数（提供时序连续性），$A_{-T_p:T_w}$ 为 HuBERT 编码的语音特征，$n$ 为扩散时间步。

为处理任意长度的输入语音，采用窗口策略：窗口长度 $T_w=100$（4秒），前置上下文 $T_p=10$。去噪网络为八层 Transformer 解码器，每层含八个注意力头，特征维度为 512。编码器与解码器之间引入对齐掩码，确保每个运动时间步仅关注对应的语音帧，防止时序错位。

### 几何损失函数

预测干净样本的设计允许直接施加几何约束，总损失函数为：

$$\mathcal{L} = \mathcal{L}_{\mathrm{simple}} + \lambda_{\mathrm{vert}} \mathcal{L}_{\mathrm{vert}} + \lambda_{\mathrm{vel}} \mathcal{L}_{\mathrm{vel}} + \lambda_{\mathrm{smooth}} \mathcal{L}_{\mathrm{smooth}} + \mathcal{L}_{\mathrm{head}}$$

各分量含义如下：

- **简单扩散损失** $\mathcal{L}_{\mathrm{simple}} = \left\| \hat{X}_{-T_p:T_w}^{0} - X_{-T_p:T_w}^{0} \right\|^2$：预测干净样本与真实干净样本的均方误差。
- **顶点位置损失** $\mathcal{L}_{\mathrm{vert}} = \left\| M_{-T_p:T_w} - \hat{M}_{-T_p:T_w} \right\|^2$：重建网格顶点与真实网格顶点的 L2 距离。
- **速度损失** $\mathcal{L}_{\mathrm{vel}} = \left\| (M_{-T_p+1:T_w} - M_{-T_p:T_w-1}) - (\hat{M}_{-T_p+1:T_w} - \hat{M}_{-T_p:T_w-1}) \right\|^2$：约束顶点运动速度的一致性，保持时序平滑。
- **平滑损失** $\mathcal{L}_{\mathrm{smooth}} = \left\| \hat{M}_{-T_p+2:T_w} - 2\hat{M}_{-T_p+1:T_w-1} + \hat{M}_{-T_p:T_w-2} \right\|^2$：惩罚顶点加速度，抑制高频抖动。
- $\mathcal{L}_{\mathrm{head}}$ 为头部运动相关的损失项。

### 说话风格编码器与对比学习

说话风格编码器从任意参考视频的运动参数序列中提取风格嵌入，其公式为：

$$\pmb{s} = SE\left( X_{0:T} \right)$$

编码器采用四层 Transformer 编码器，含四个注意力头，输出特征维度 $d_s=128$，输入序列长度 100 帧（4秒）。风格嵌入通过 NT-Xent 对比损失进行训练：

$$\mathcal{L}_{i,j} = -\log \frac{\exp( \cos\_\sin(s_i, s_j) / \tau )}{\sum_{k=1}^{2N_s} \mathbf{1}_{k \neq i} \exp( \cos\_\sin(s_i, s_k) / \tau )}$$

其中 $\tau=0.1$ 为温度参数。该损失最大化同一样本不同片段的正样本对相似度，最小化不同样本的负样本对相似度，使风格嵌入仅捕获说话风格信息而与身份无关。

加入风格和形状条件后，去噪网络的完整输出为：

$$\hat{X}_{-T_p;T_w}^{0} = D\left( X_{0:T_w}^{n}, X_{-T_p:0}^{0}, A_{-T_p:T_w}, s, \beta, n \right)$$

### 无分类器引导采样

推理阶段采用增量式无分类器引导，分别控制语音和风格条件的影响强度：

$$\hat{X}^{0} = D(X^n,\emptyset,\emptyset,\beta,n) + w_a\left[D(X^n,A,\emptyset,\beta,n)-D(X^n,\emptyset,\emptyset,\beta,n)\right] + w_s\left[D(X^n,A,s,\beta,n)-D(X^n,A,\emptyset,\beta,n)\right]$$

其中 $w_a$ 为语音引导权重，$w_s$ 为风格引导权重。通过调整这两个权重，可在推理时灵活控制生成结果对语音内容的遵从程度和风格化程度，实现个性化和多样化的面部动画生成。

![[assets/figures/papers/paper_list_l1923_DiffPoseTalk_Speech_Driven_Stylistic_3D_Facial_Animation_and_Head_Pose_G/figures/002_Figure_2.jpg]]
*Figure 2: (Left) Transformer-based denoising network. We employ a windowing strategy to generate speech-driven 3D facial animations for inputs of arbitrary length. HuBERT-encoded speech features*

## 实验与关键发现

### 实验设置

DiffPoseTalk 在 **TFHP** 数据集上进行训练和评估。该数据集包含 1,052 个视频，涵盖 588 位说话人，总时长约 26.5 小时。数据按说话人划分：460 人用于训练，64 人用于验证，64 人用于测试。

说话风格编码器采用 4 层 Transformer 编码器，配备 4 个注意力头，风格特征维度 $d_s = 128$，输入序列长度设为 100 帧（约 4 秒），对比学习温度 $\tau = 0.1$。去噪网络采用 8 层 Transformer 解码器，配备 8 个注意力头，特征维度为 512，窗口长度 $T_w = 100$，前序帧 $T_p = 10$。

### 定量评估

在 TFHP 测试集上，DiffPoseTalk 在唇同步、面部动态、口型偏差和头部姿态节拍对齐四项指标上全面超越现有方法（见表 1）。核心结果如下：

- **唇同步精度（LVE）**：DiffPoseTalk 取得 **8.94**，显著优于 FaceDiffuser（MIG 2023）等扩散基线及 CodeTalker（CVPR 2023）、FaceFormer（CVPR 2022）等确定性方法。LVE 越低表示唇部顶点与真实值偏差越小。
- **面部动态偏差（FDD）**：DiffPoseTalk 取得 **9.60**，在所有方法中最低。FDD 衡量生成运动与真实运动在动态特征空间的距离，低值表明生成的表情变化模式更接近真实说话风格。
- **口型开合偏差（MOD）**：DiffPoseTalk 取得 **1.62**，同样为最优。MOD 直接度量嘴部开合程度与语音的匹配精度。
- **头部姿态节拍对齐（BA）**：DiffPoseTalk 取得 **0.29**（越高越好），表明生成的头部运动与语音节拍高度一致。

值得注意的是，即使在不预测头部姿态的变体（Ours no HP）中，DiffPoseTalk 在 LVE 上仍达到 **8.81**，FDD 为 **10.13**，MOD 为 **1.72**，均优于其他对比方法。这验证了扩散模型本身在面部动画生成上的优势。

### 消融实验

为验证各核心组件的贡献，论文进行了系统的消融实验（见表 1），揭示了以下因果机制：

**1. 说话风格编码器（SSE）是关键瓶颈。** 移除风格编码器（Ours w/o SSE）导致所有指标显著下降，尤其 FDD 和 MOD 恶化明显。这表明基于对比学习的风格嵌入是捕捉个性化说话风格的核心组件，缺少它将使模型退化为风格无关的确定性生成，无法再现说话人的独特面部动态。

**2. 几何损失对精确动画不可或缺。** 移除所有几何损失（Ours w/o Lgeom）后，模型无法生成精确的面部动画。这证实了预测干净样本 $X^0$ 而非噪声的设计选择具有实际价值——正是这一选择使得在去噪网络上施加顶点损失 $\mathcal{L}_{\text{vert}}$、速度损失 $\mathcal{L}_{\text{vel}}$ 和平滑损失 $\mathcal{L}_{\text{smooth}}$ 成为可能，从而为面部运动提供了更精细的约束。

**3. 对齐掩码保证时序同步。** 移除对齐掩码（Ours w/o AM）导致严重的音频-视频不同步问题。对齐掩码确保运动时间步仅关注对应的语音帧，是维持唇同步的底层机制。

**4. 无分类器引导（CFG）对唇同步有正向贡献。** 排除 CFG（Ours w/o CFG）对 LVE 产生负面影响，但在 FDD 和 MOD 上略有改善。这表明 CFG 通过增强对语音条件的遵从性来提升唇同步精度，但过强的引导可能略微抑制风格多样性。增量式引导策略（分别控制语音权重 $w_a$ 和风格权重 $w_s$）提供了在同步性与表现力之间权衡的灵活机制。

### 用户研究

论文通过用户研究验证生成结果的主观质量。31 名参与者对生成的视频在口型同步、风格相似度和自然度三个维度进行盲评（见表 2）。DiffPoseTalk 在所有维度上均获得最高评分，与定量指标的结果一致，表明该方法在感知质量上也具有显著优势。

### 定性比较

在定性比较中（图 3、图 4），DiffPoseTalk 生成的唇部运动更清晰、与语音更同步，同时能有效捕捉不同说话人的风格特征（如嘴部张合幅度、面部动态节奏）。在包含头部姿态预测的场景中（图 4），DiffPoseTalk 的头部运动与语音节拍（图中 `>` 标记的重音位置）对齐更好，增强了整体表现力。

### 失败模式与局限性

尽管 DiffPoseTalk 取得了领先性能，但存在以下已知局限：

1. **推理效率**：去噪过程是顺序执行的，推理计算成本较高。论文指出可探索 DPM-Solver++ 等高级去噪器加速采样。
2. **噪声鲁棒性**：当输入音频包含极高噪声时，模型可能生成模糊或过度平滑的唇部动作。
3. **口腔内部缺失**：当前方法仅建模人脸表面形状，忽略了牙齿和舌头的建模，限制了完整说话人脸的真实感。
4. **数据覆盖不足**：缺乏大规模真实世界 3D 说话数据集，限制了模型对更广泛风格和身份的泛化能力。

![[assets/figures/papers/paper_list_l1923_DiffPoseTalk_Speech_Driven_Stylistic_3D_Facial_Animation_and_Head_Pose_G/figures/003_Table_1.jpg]]
*Table 1: Quantitative evaluation of the comparative methods, our proposed method, and ablation study variants. We run the evaluation 10 times and report the average score with a 95% confidence interval when applicable. We also report the diversity scores of expression and head pose generation. Note that the vertex-related metrics are not comparable with SadTalker due to its different face topology*

![[assets/figures/papers/paper_list_l1923_DiffPoseTalk_Speech_Driven_Stylistic_3D_Facial_Animation_and_Head_Pose_G/figures/004_Table_2.jpg]]
*Table 2: User study results*

![[assets/figures/papers/paper_list_l1923_DiffPoseTalk_Speech_Driven_Stylistic_3D_Facial_Animation_and_Head_Pose_G/figures/005_Figure_3.jpg]]
*Figure 3: Qualitative comparison with the state of the arts (w/o head pose prediction). Results of different identities are split by dashed lines*

![[assets/figures/papers/paper_list_l1923_DiffPoseTalk_Speech_Driven_Stylistic_3D_Facial_Animation_and_Head_Pose_G/figures/006_Figure_4.jpg]]
*Figure 4: Qualitative comparison with the state of the arts (w/ head pose prediction). Results of different identities are split by dashed lines. The “>” indicates stress in speech*

## 定位与知识库关联

DiffPoseTalk 处于语音驱动 3D 面部动画从确定性回归向概率生成建模过渡的关键节点。其核心突破在于用**扩散概率模型**替代传统的确定性映射，从而捕捉语音到面部动作的“多对多”映射关系——这一瓶颈长期困扰着基于回归的方法，导致动作过度平滑和均值回归。

### 与现有方法的层级关系

**确定性回归基线。** 早期工作如 **FaceFormer**（Fan et al., CVPR 2022）建立了基于 Transformer 的语音到面部动作直接映射范式，但其确定性本质限制了生成多样性。**CodeTalker**（Xing et al., CVPR 2023）引入离散动作先验来缓解这一问题，但仍在离散码本空间内运作，无法完全摆脱均值回归。DiffPoseTalk 继承了 FaceFormer 的注意力对齐架构（对齐掩码机制），但将整个生成过程重构为扩散模型的迭代去噪，从根本上改变了动作空间的探索方式。

**扩散语音驱动动画。** **FaceDiffuser**（Stan et al., MIG 2023）是最近将扩散模型引入该领域的代表工作。DiffPoseTalk 与其共享扩散建模的基本思路，但在三个关键维度上形成差异化：（1）**去噪目标**——DiffPoseTalk 预测干净样本 $X^0$ 而非噪声，这使得可以直接添加几何损失（顶点损失、速度损失、平滑损失）作为精确的运动约束；（2）**风格泛化**——FaceDiffuser 依赖固定的风格标签，而 DiffPoseTalk 通过对比学习训练风格编码器，从任意参考视频中提取风格嵌入，无需针对新说话人微调；（3）**头部姿态联合生成**——DiffPoseTalk 同时生成头部姿态，并通过节拍对齐指标（BA）进行显式评估。

**风格化与个性化方法。** **Imitator**（Thambiraja et al., ICCV 2023）和 **EmoTalk**（Peng et al., ICCV 2023）分别从示例驱动和情感标签角度探索个性化生成。DiffPoseTalk 的风格编码器采用了更通用的对比学习框架（NT-Xent 损失），将风格定义为身份无关的嵌入向量，在训练时从未见过的新说话人上也能泛化。**SadTalker**（Zhang et al., CVPR 2023）从单张图像生成 3D 说话人脸，但使用不同的人脸拓扑，无法直接与基于 FLAME 的方法进行顶点级指标比较。

### 适用边界与局限

**推理效率边界。** 扩散模型的反向去噪过程是顺序执行的（通常需要数十到数百步），这导致推理计算成本显著高于单步前向的确定性模型。论文明确指出这一限制，并建议未来探索 DPM-Solver++ 等高级 ODE 求解器来加速采样。对于需要实时交互的应用场景（如虚拟对话助手），当前推理速度可能构成瓶颈。

**音频质量敏感性。** 当输入语音包含极高噪声时，模型可能产生模糊或过度平滑的唇部动作。这表明去噪网络在低信噪比条件下难以从 HuBERT 特征中提取可靠的语音-发音映射，需要进一步验证其对真实世界噪声环境的鲁棒性。

**解剖学建模不完整。** 当前方法仅关注面部表面（FLAME 网格的 5023 个顶点），完全忽略了口腔内部结构——牙齿和舌头的建模。这使得生成的动画在张嘴说话时缺乏口腔内部的视觉真实感，在特写镜头或高保真渲染场景下可能暴露不足。

**数据规模与多样性限制。** TFHP 数据集包含 588 个说话人的 26.5 小时视频，虽已是大规模 3D 说话人脸数据集，但相较于真实世界中的人类多样性仍显有限。风格编码器的泛化能力受限于训练数据的风格覆盖范围，极端或高度风格化的说话方式可能超出分布。

### 开放问题与未来方向

1. **实时推理**：如何通过蒸馏、步长缩减或专用求解器将扩散采样加速至实时？这是从学术演示走向实际部署的关键工程挑战。

2. **噪声鲁棒性**：能否通过数据增强（添加背景噪声、混响）或多模态融合（引入视频信息）增强对低质量音频的容错能力？

3. **完整口腔建模**：将牙齿、舌头等口腔内部结构纳入 3D 表示（如使用 FLAME 的扩展模型或显式口腔网格），实现真正完整的说话人脸动画。

4. **规模化数据**：如何构建涵盖更多语言、口音、年龄组和情感风格的 3D 真实说话数据集？半监督或自监督的 3D 重建管线可能是可行路径。

5. **多模态风格解耦**：当前风格编码器从运动序列中提取整体风格嵌入，未来可探索将风格进一步解耦为节奏模式、表情幅度、头部运动偏好等可解释维度，实现更精细的风格编辑与迁移。

## 原文 PDF

![[paperPDFs/SIGGRAPH_2024/DiffPoseTalk_Speech_Driven_Stylistic_3D_Facial_Animation_and_Head_Pose_Generation_via_Diffusion_Models.pdf]]

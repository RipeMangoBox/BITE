---
title: "Face2Scene: Using Facial Degradation as an Oracle for Diffusion-Based Scene Restoration"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Face2Scene_Using_Facial_Degradation_as_an_Oracle_for_Diffusion_Based_Scene_Restoration.pdf
project_link: null
code_link: null
aliases:
- Face2Scene
tags:
- CVPR_2026
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
core_operator: 利用参考面部恢复模型从同一身份的低质量-高质量面部对中提取准确的退化代码（FaDeX），并通过MapNet将其转化为多尺度条件令牌注入扩散模型，从而为全场景恢复提供可靠的退化先验。
primary_logic: 将人脸视为退化的“预言机”——从信号最强、几何最稳定且常有身份参考的面部区域精确推断全局退化，并用该退化代码指导一次性扩散模型修复整个人物场景，从而将参考面部修复、场景级增强与退化感知扩散统一在一个框架内。
claims:
- Face2Scene 在 InScene 合成与真实验证集上全面优于所有对比方法，在 DISTS、LPIPS、MUSIQ 等多个指标上取得显著提升。
- 使用退化估计的 Face2Scene 在所有指标上均优于不使用退化估计的变体 (10/10 vs 0/10)，证明了面部退化代码的有效性。
- 在插入真实人脸后，Face2Scene 在非人脸区域仍然优于 S3Diff，10 项指标中赢得 8 项，表明退化信息被成功传递到场景其他部分。
- FaDeX 提取的退化嵌入在不同图像间对相同退化类型保持高相似性，而对不同退化类型具有低相似性，证实其成功解耦退化与内容。
---

# Face2Scene: Using Facial Degradation as an Oracle for Diffusion-Based Scene Restoration

> [!tip] 核心洞察
> 将人脸视为退化的“预言机”——从信号最强、几何最稳定且常有身份参考的面部区域精确推断全局退化，并用该退化代码指导一次性扩散模型修复整个人物场景，从而将参考面部修复、场景级增强与退化感知扩散统一在一个框架内。

| 字段 | 内容 |
|------|------|
| 中文题名 | Face2Scene：以面部退化作为先知指导基于扩散的场景恢复 |
| 英文题名 | Face2Scene: Using Facial Degradation as an Oracle for Diffusion-Based Scene Restoration |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Kazerouni_Face2Scene_Using_Facial_Degradation_as_an_Oracle_for_Diffusion-Based_Scene_CVPR_2026_paper.html) |
| Topic | #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video |
| Method | Face2Scene |
| Dataset | InScene synthetic validation set, InScene real validation set |

> [!tip] 效果简介
> - InScene synthetic validation set 上，DISTS↓ 0.1007 vs 优于所有对比方法 (最佳)；LPIPS↓ 0.2421 vs 优于所有对比方法 (最佳)；FID↓ 15.26 vs 优于所有对比方法 (最佳)。
> - InScene real validation set 上，DISTS↓, LPIPS↓, MUSIQ↑, CLIP-IQA↑, MANIQA↑ 全面最佳 vs 所有对比方法 (大幅领先)。

## 概要

全场景图像恢复旨在从退化的低质量输入中重建高质量的人物图像。现有方法通常直接从退化图像中盲估计全局退化参数（如噪声水平、模糊程度），但这一过程本质上是不适定的——在缺乏先验的条件下，模型难以准确区分退化与内容，导致恢复结果出现纹理失真、伪影或细节丢失。

**Face2Scene** 提出了一种全新的解决思路：将人脸视为退化的“预言机”（oracle）。其核心洞察在于，人脸区域信号最强、几何结构最稳定，且同一身份往往存在高质量参考图像，因此可以从人脸区域精确推断出全局退化信息，再将这一退化代码传递给扩散模型，指导整个人物场景的一次性恢复。

该方法采用两阶段框架。第一阶段利用现成的参考面部修复模型（Ref-FR），结合身份参考图像，将低质量人脸重建为高质量人脸，从而获得一对对齐的 LQ-HQ 面部对。第二阶段引入 **FaDeX**（Face-derived Degradation eXtractor），从该面部对中提取与图像内容解耦的退化嵌入；随后通过 **MapNet** 将退化特征转化为 21 个多尺度条件令牌，经交叉注意力注入 SD-Turbo 一步扩散模型，完成从面部到全身、从前景到背景的全场景恢复。

实验结果表明，Face2Scene 在 InScene 合成验证集与真实验证集上均显著优于现有方法，在 DISTS、LPIPS、FID 等全参考指标以及 MUSIQ、CLIP-IQA、MANIQA 等无参考感知质量指标上取得全面领先。消融实验进一步证实：引入 FaDeX 退化估计后，模型在所有指标上均优于无退化估计的变体；即使在非人脸区域，退化信息仍能有效传递并指导恢复，验证了“面部作为退化预言机”这一核心假设的有效性。

### 全场景图像恢复的根本瓶颈

图像恢复旨在从低质量（LQ）观测中重建高质量（HQ）图像，是一个典型的病态逆问题。当退化类型未知且复杂时——例如同时存在噪声、模糊、压缩伪影等多种退化因素——恢复难度急剧上升。现有全场景恢复方法面临一个共同的根本瓶颈：**缺乏对退化过程的精确估计**。大多数方法要么完全忽略退化建模，直接从 LQ 输入学习到 HQ 输出的映射；要么仅使用粗粒度的全局退化表示，例如预测一两个标量值来描述噪声水平或模糊核宽度。

这种退化信息的缺失或粗糙化，使得恢复问题高度欠定。模型不得不同时推断“图像应该是什么”和“图像是如何被破坏的”，导致在复杂真实退化下容易产生视觉伪影、纹理幻觉或细节丢失。尤其在包含人脸、人体、背景等多种语义区域的全身场景中，不同区域对退化的敏感度和恢复要求各异，统一的盲恢复策略往往顾此失彼。

### 现有方法的缺口

当前全场景图像恢复方法可大致分为三类，各有明显局限：

- **通用盲复原方法**（如 **Real-ESRGAN**、**DiffBIR**）在训练时覆盖多种合成退化，但在推理时无法感知具体退化类型，本质上是在退化空间上求平均解，难以针对特定退化做出最优恢复。
- **退化引导方法**（如 **S3Diff**）尝试显式建模退化，但仅使用全局低维标量（噪声水平、模糊程度）作为条件，缺乏空间和语义上的退化细节，无法捕捉复杂退化的全部特征。
- **人脸特化方法**利用面部先验进行高质量修复，但仅限于面部区域，无法将恢复能力扩展到人体和背景，导致全场景中人脸与其他区域的质量严重不匹配。

一个关键观察是：**人脸是场景中最具信息密度的区域**。人脸具有高度结构化的几何形态、丰富的纹理细节，且人类对人脸质量的感知极为敏感。更重要的是，在许多实际应用中（如老照片修复、监控增强），同一身份往往存在多张参考图像，为人脸修复提供了额外的身份先验。然而，现有方法未能将面部区域获得的精确退化信息有效传递到整个场景。

### Face2Scene 的核心动机

Face2Scene 的核心洞察是：**将人脸视为退化的“预言机”（oracle）**。具体而言：

1. **面部是退化估计的最佳窗口**：人脸区域信号强、几何结构稳定，且常有多张身份参考图像可用。通过现成的参考面部修复模型（Ref-FR），可以从同一身份的 LQ-HQ 面部对中精确推断出退化过程——包括噪声类型、模糊程度、压缩强度等属性。
2. **退化信息可跨区域传递**：一旦从面部提取出准确的退化表示，该退化代码可以作为全局条件，指导扩散模型一次性修复整个人物场景（面部、身体、背景），从而将参考面部修复、场景级增强与退化感知扩散统一在一个框架内。
3. **退化与内容解耦是关键**：退化表示必须与图像内容无关，才能可靠地从面部区域推广到场景其他部分。这要求退化提取器（FaDeX）学习一个内容无关的退化嵌入空间。

### 技术挑战

实现上述动机面临两个核心技术挑战：

- **如何从 LQ-HQ 面部对中提取内容无关的退化代码？** 需要一个专门的退化提取器，在对比学习框架下强制相同退化类型的嵌入相互靠近、不同退化类型的嵌入相互远离，从而解耦退化与面部身份、姿态、表情等内容因素。
- **如何将面部退化代码有效注入全场景扩散模型？** 仅使用低维全局标量不足以描述复杂退化，需要设计一个退化映射网络（MapNet），将空间退化特征转化为多尺度条件令牌，通过交叉注意力机制注入 SD-Turbo 一次性扩散恢复器，为去噪过程提供丰富的退化上下文。

### 与现有工作的本质区别

与 **S3Diff** 等退化引导方法相比，Face2Scene 的退化估计来源发生了根本性转变：不再从低质量输入图像本身盲估计退化（仅预测噪声和模糊两个全局标量），而是**利用外部身份参考**，从参考面部修复模型生成的 LQ-HQ 面部对中提取退化代码。这使得退化估计更加精确可靠，因为参考图像提供了额外的干净信号源。同时，退化表示从低维标量升级为多尺度空间令牌（21 个令牌），能够传递更丰富的退化上下文，指导扩散模型做出更精准的恢复决策。

## 核心方法与创新机理

Face2Scene 的核心创新在于将人脸作为退化“预言机”，从信号最强、几何最稳定且常具身份参考的面部区域精确推断全局退化，并以此指导一次性扩散模型修复包含人物、衣着、背景在内的完整场景。这一范式通过两个关键的 **changed slots** 实现，从根本上区别于现有方法。

### 退化估计来源：从盲估计到身份参考驱动的面部退化代码

现有场景恢复方法大多直接从低质量输入图像中盲估计退化信息，这一过程高度欠定，尤其在复杂真实退化下难以准确建模。例如，**S3Diff** 仅预测两个全局标量（噪声和模糊程度）作为退化表示；**DeeDSR** 则依赖无监督对比学习从单张低质图像中提取退化编码，但缺乏高质量参考信号。

Face2Scene 改变了这一范式：它利用现成的参考面部修复模型（Ref-FR），从同一身份的 **LQ-HQ 面部对** 中提取退化代码。具体而言，第一阶段将检测到的面部裁剪并刚体对齐至规范帧，Ref-FR 模型基于身份参考图像集重建高质量面部；第二阶段，FaDeX（Face-derived Degradation eXtractor）以通道拼接的 HQ-LQ 面部对为输入，通过轻量卷积编码器输出面部退化嵌入 $Z_{\mathrm{face}}$。这一设计的关键优势在于：面部区域纹理丰富、结构规整，且身份参考图像提供了额外的监督信号，使得退化估计比从全场景盲推断更为可靠。

### 退化表示与注入方式：从全局标量到多尺度空间感知令牌

退化信息如何注入恢复模型是另一个关键差异点。**S3Diff** 将全局标量退化参数通过调制 LoRA 权重的方式注入扩散模型，信息容量有限且缺乏空间感知能力。其他基线如 **DiffBIR**、**Real-ESRGAN** 则未显式注入退化信息。

Face2Scene 通过 MapNet 将 FaDeX 的空间退化特征转化为 **21 个多尺度退化令牌**，并通过交叉注意力注入 SD-Turbo 一次性扩散恢复器。MapNet 的处理流程为：首先对 $Z_{\mathrm{face}}$ 施加重叠块嵌入（3×3 卷积，步长 2）和 LayerNorm 得到令牌序列 $F$，再通过残差注意力模块（DegAttn）增强退化相关特征；随后分别进行 4×4、2×2 和 1×1 的网格平均池化，产生 16+4+1=21 个令牌。这些令牌与通用正面文本提示令牌拼接后，通过 Stable Diffusion 的交叉注意力机制条件化一步扩散过程，显式传递退化的类型与严重程度。

与全局标量相比，多尺度令牌设计具有三重优势：（1）**空间感知**——不同位置的令牌保留了退化特征的空间分布信息；（2）**多尺度表达**——从细粒度到全局的多层池化使模型能同时捕捉局部纹理退化和全局噪声/模糊特性；（3）**高信息容量**——21 个令牌可编码比两个标量丰富得多的退化上下文。

### 因果机制与证据强度

上述两个 changed slots 共同构成了 Face2Scene 的核心因果链：**精确退化估计（FaDeX）→ 丰富退化表示（MapNet 令牌）→ 可靠的全场景恢复**。消融实验为这一链条提供了强有力支持：

- **退化估计的必要性**（Table 3）：使用 FaDeX 退化估计的 Face2Scene 在所有 10 项指标上均优于不使用退化估计的变体（10/10 vs 0/10），证明面部退化代码是性能的决定性因素。
- **退化信息的场景传递**（Table 3）：将真实人脸插入恢复图像以隔离非人脸区域后，Face2Scene 在 10 项指标中的 8 项仍优于 S3Diff，表明退化信息成功从面部传递到衣着、背景等场景其他部分。
- **退化与内容的解耦**（Figure 4）：余弦相似度分析显示，FaDeX 嵌入在相同退化类型的不同图像间保持高相似性，而在不同退化类型间相似度低，证实其成功将退化信息与图像内容解耦。

### 失败模式与边界条件

尽管创新显著，Face2Scene 存在两个关键边界条件：
1. **空间一致性假设**：FaDeX 从面部区域提取的退化代码隐含假设退化在整幅图像中空间一致，无法处理局部变化的退化（如运动模糊仅影响移动主体、景深效果使背景模糊而面部清晰）。
2. **参考依赖瓶颈**：退化估计的质量受限于现成 Ref-FR 模型的性能；若面部恢复不准确，FaDeX 的退化代码将包含误差。此外，对身份参考图像的依赖限制了无参考场景下的应用。

Face2Scene 采用两阶段流水线，将人脸视为退化的“预言机”，利用面部区域精确估计退化信息，再将其作为条件注入一次性扩散模型，完成全场景恢复。

**阶段一：参考面部修复。** 给定低质量全场景图像 $I^{\mathrm{LQ}}$，首先检测人脸并提取方形裁剪块 $x^{\mathrm{LQ}}$，估计刚体对齐变换后将裁剪块映射到规范帧并缩放至 512×512。随后，一个现成的参考面部修复模型（Ref-FR）$F_{\theta}$ 结合身份参考图像集 $\{x_k^{\mathrm{ref}}\}$，在规范帧中生成高质量面部重建 $\tilde{x}^{\mathrm{HQ}}$：

$$\tilde{x}^{\mathrm{HQ}} = F_{\theta}(\tilde{x}^{\mathrm{LQ}}, \{x_k^{\mathrm{ref}}\})$$

这一阶段的核心产出是一对对齐的 LQ-HQ 面部图像，为后续退化估计提供精确的信号对比。

**阶段二：退化感知的全场景恢复。** 该阶段包含三个紧密耦合的模块：

1. **FaDeX（面部退化提取器）**：以通道拼接的 HQ 与 LQ 面部图像为输入，通过轻量卷积编码器 $E_{\phi}$ 提取空间退化特征 $Z_{\mathrm{face}}$。FaDeX 通过对比损失 $\mathcal{L}_{\mathrm{Deg}}$ 训练，使相同退化算子的样本嵌入相互吸引、不同退化的相互排斥，从而将退化属性与图像内容解耦。

2. **MapNet（退化映射网络）**：将 FaDeX 输出的空间特征转化为紧凑的多尺度条件令牌。具体流程为：先通过重叠块嵌入（3×3 卷积，步长 2，接 LayerNorm）将 $Z_{\mathrm{face}}$ 序列化为 $F \in \mathbb{R}^{H' \times W' \times C}$，再经残差注意力模块（DegAttn）增强退化感知表示，最后通过网格平均池化（GAP 4×4、2×2、1×1）生成 16+4+1=21 个多尺度退化令牌。

3. **SD-Turbo 一次性扩散恢复器**：将 21 个退化令牌与通用正向文本令牌拼接，通过交叉注意力注入 SD-Turbo 扩散模型。模型以低质量全场景图像和退化令牌为条件，仅需一次去噪步骤即可生成恢复后的全场景图像 $\hat{I}$。

整个框架的端到端训练由重建损失与对抗损失加权驱动：

$$\mathcal{L}_{\mathrm{rec}} = \lambda_2 \|\hat{I} - I^{\mathrm{HQ}}\|_2^2 + \lambda_{\mathrm{LPIPS}} \mathrm{LPIPS}(\hat{I}, I^{\mathrm{HQ}})$$

$$\mathcal{L}(\theta) = \mathcal{L}_{\mathrm{rec}} + \lambda_{\mathrm{GAN}} \mathcal{L}_{\mathrm{GAN}}$$

**输入输出流总结：** 输入为低质量全场景图像与身份参考面部图像集，经阶段一产出 LQ-HQ 面部对，阶段二以该面部对提取退化代码并映射为多尺度令牌，最终由 SD-Turbo 一次性输出高质量全场景恢复图像。退化信息从面部区域提取后，通过交叉注意力机制传递至整个人物场景（面部、身体、背景），实现了“以面部为预言机”的核心设计理念。

![[assets/figures/papers/paper_list_l2483_https_openaccess_thecvf_com_content_CVPR2026_html_Kazerouni_Face2Scene_U/figures/001_Figure_1.jpg]]
*Figure 1: Overview of Face2Scene. We infer a face-derived degradation code from identity references and the observed LQ face, then use it as oracle guidance to restore the full scene (face, body, background) with a one-step diffusion restorer*

![[assets/figures/papers/paper_list_l2483_https_openaccess_thecvf_com_content_CVPR2026_html_Kazerouni_Face2Scene_U/figures/002_Figure_2.jpg]]
*Figure 2: Overview of the Face2Scene pipeline. In stage I, we leverage a set of reference faces to restore the LQ face crop. In stage II, we use the pair of LQ and HQ faces to extract a guided degradation with FaDeX and inject it into a one-step diffusion model using MapNet. The diffusion model then reconstructs the full-scene image*

Face2Scene 的核心架构由两条解耦的功能链路构成：**退化感知链路**（FaDeX + MapNet）负责从面部区域提取并编码全局退化信息，**一次性扩散恢复链路**（SD-Turbo）负责在退化条件的引导下完成全场景重建。两条链路通过多尺度交叉注意力机制桥接，使得从面部“预言机”中提取的退化代码能够精确指导整个人物场景（面部、身体、背景）的统一恢复。

### FaDeX：面部退化提取器

FaDeX 的设计目标是从参考面部修复模型生成的 LQ-HQ 面部对中提取与图像内容解耦的退化嵌入。其输入为通道级拼接的低质量面部 $x^{\mathrm{LQ}}$ 与高质量重建面部 $\tilde{x}^{\mathrm{HQ}}$，经轻量级卷积编码器 $E_{\phi}$ 处理后输出空间退化特征图 $Z_{\mathrm{face}} \in \mathbb{R}^{C \times H' \times W'}$。

为强制退化嵌入与内容解耦，FaDeX 采用对比学习策略，损失函数定义为：

$$\mathcal{L}_{\mathrm{Deg}} = \sum_{i\in\mathcal{B}} \sum_{p\in\mathcal{P}(i)} -\log \frac{\exp(\langle q_i, q_p \rangle / \tau)}{\sum_{a\in\mathcal{P}(i)\cup\mathcal{N}(i)} \exp(\langle q_i, q_a \rangle / \tau)}$$

其中 $q_i = g_{\psi}(\mathrm{GAP}(Z_{\mathrm{face}}^{(i)}))$ 为经全局平均池化和 MLP 投影头 $g_{\psi}$ 处理后的退化嵌入向量，$\mathcal{P}(i)$ 表示与样本 $i$ 施加相同退化算子的正样本集合，$\mathcal{N}(i)$ 为施加不同退化的负样本集合，$\tau$ 为温度系数。该损失使相同退化类型的嵌入相互吸引、不同退化类型的嵌入相互排斥，从而学习到与图像内容无关的退化判别表示。

### MapNet：退化映射网络

MapNet 将 FaDeX 输出的空间退化特征 $Z_{\mathrm{face}}$ 转化为一组紧凑的多尺度条件令牌，用于注入扩散模型。其处理流程如下：

1. **重叠块嵌入**：通过 $3 \times 3$ 卷积（步长 2）加 LayerNorm 将 $Z_{\mathrm{face}}$ 转化为令牌序列 $F \in \mathbb{R}^{N \times D}$。
2. **残差注意力精炼**：设计 DegAttn 模块对令牌序列进行上下文增强，捕获退化特征的空间依赖关系。
3. **多尺度池化聚合**：对精炼后的特征图分别施加 $4 \times 4$、$2 \times 2$、$1 \times 1$ 的网格平均池化，产生 16 + 4 + 1 = 21 个多尺度退化令牌。

这 21 个令牌与通用正向文本提示令牌拼接后，通过 SD-Turbo 的交叉注意力层注入扩散去噪过程，为恢复器提供从粗粒度到细粒度的退化上下文信息。

### 一次性扩散恢复器与训练损失

恢复器基于 SD-Turbo 构建，接受低质量全场景图像 $I^{\mathrm{LQ}}$ 与 MapNet 输出的多尺度退化令牌，通过单步去噪生成恢复图像 $\hat{I}$。训练损失由重建损失与对抗损失加权组合：

$$\mathcal{L}_{\mathrm{rec}} = \lambda_2 \|\hat{I} - I^{\mathrm{HQ}}\|_2^2 + \lambda_{\mathrm{LPIPS}} \mathrm{LPIPS}(\hat{I}, I^{\mathrm{HQ}})$$

$$\mathcal{L}(\theta) = \mathcal{L}_{\mathrm{rec}} + \lambda_{\mathrm{GAN}} \mathcal{L}_{\mathrm{GAN}}$$

重建损失结合像素级 L2 保真度与深度感知 LPIPS 损失，确保恢复图像在像素和感知层面均逼近高质量目标。对抗损失 $\mathcal{L}_{\mathrm{GAN}}$ 通过判别器 $D_{\phi}$ 与生成器 $G_{\theta}$ 的对抗训练提升恢复图像的分布真实感，其具体形式为标准 GAN 目标函数。$\lambda_2$、$\lambda_{\mathrm{LPIPS}}$、$\lambda_{\mathrm{GAN}}$ 为平衡各项贡献的超参数。

### 退化嵌入解耦验证

FaDeX 学习到的退化嵌入质量通过余弦相似度分析验证（Figure 4）：对相同退化类型的不同图像，嵌入间余弦相似度较高；对不同退化类型的图像，相似度则显著降低。这一实验结果证实 FaDeX 成功将退化属性与图像内容解耦，为后续 MapNet 的条件注入提供了可靠且纯净的退化先验。

![[assets/figures/papers/paper_list_l2483_https_openaccess_thecvf_com_content_CVPR2026_html_Kazerouni_Face2Scene_U/figures/005_Figure_4.jpg]]
*Figure 4: Cosine similarity analysis. We show the cosine similarity across embeddings of image pairs with different degradations. (Left) similarities per degradation type (averaged over images). (Right) similarities per image, averaged over degradation types. Shaded area shows standard deviation. This confirms FaDeX isolates degradation from image content*

## 实验与关键发现

### 实验设置

**数据集构建。** Face2Scene 基于自建的 InScene 数据集进行训练与评估，该数据集包含 57,449 张图像，来自 1,819 个身份。训练集分为无参考数据与参考数据（合成+真实）两部分；测试集包含合成验证集、真实验证集与真实测试集。合成数据通过对 HQ 图像施加多种退化算子（噪声、模糊、压缩等）生成 LQ 配对，真实数据则通过质量筛选获得。完整的数据划分与各子集的平均质量分数见 Table 1。

**训练细节。** 模型训练 20K 次迭代，有效批次大小为 64，使用 8 张 A100 GPU，学习率设为 $2\times10^{-5}$。基础扩散模型采用 SD-Turbo，在退化感知条件下进行微调。FaDeX 的对比损失温度参数 $\tau$ 按标准对比学习设置，重建损失中 $\lambda_2$ 与 $\lambda_{\text{LPIPS}}$ 以及对抗损失权重 $\lambda_{\text{GAN}}$ 通过验证集调优确定。

**评估指标。** 采用全参考指标 DISTS、LPIPS、FID 评估像素与分布保真度，采用无参考指标 MUSIQ、CLIP-IQA、MANIQA 评估感知质量。合成验证集具备 GT 图像，可使用全参考指标；真实验证集仅使用无参考指标。

**对比基线。** 选取六类代表性方法：通用盲复原 **Real-ESRGAN**、一步扩散复原 **OSED**、扩散盲复原 **DiffBIR**、退化引导一步扩散 **S3Diff**（预测全局噪声/模糊标量）、无监督退化编码 **DeeDSR** 以及人体感知一步扩散 **HAODiff**。其中 S3Diff 是最直接的退化感知对比，因其同样采用一步扩散并显式注入退化信息。

### 主实验结果

**合成验证集。** Table 2 展示了 InScene 合成验证集上的定量对比。Face2Scene 在 DISTS（0.1007）、LPIPS（0.2421）、FID（15.26）三项全参考指标上均取得最优，同时在 MUSIQ、CLIP-IQA、MANIQA 等无参考感知指标上也全面领先。相较 S3Diff 的全局标量退化表示，Face2Scene 的多尺度退化令牌提供了更丰富的退化上下文，使恢复图像在纹理保真度与感知自然度之间取得更好平衡。

**真实验证集。** 在真实退化场景下，Face2Scene 的优势进一步扩大——在所有对比方法中，DISTS、LPIPS、MUSIQ、CLIP-IQA、MANIQA 五项指标均大幅领先。这一结果表明，从面部区域精确估计退化并将其注入扩散模型，对于处理真实世界中复杂、未知的退化分布具有决定性作用。Figure 3 的视觉对比进一步印证了定量结果：Face2Scene 在面部细节、衣物纹理和背景结构上均展现出更少的伪影与更高的真实感。

### 消融实验

**退化估计的必要性。** Table 3 最后两行直接对比了有无 FaDeX 退化估计的变体。结果表明，引入退化估计后，模型在全部 10 项指标上均取得提升，证实面部退化代码是 Face2Scene 性能的核心驱动力。移除退化估计后，扩散模型仅依赖 LQ 图像本身进行恢复，退化信息不足导致输出出现过度平滑或伪影残留。

**退化信息的场景传递。** 为验证退化代码是否真正指导了全场景恢复（而非仅提升面部区域），作者设计了“GT Face Inserted”实验：将恢复图像中的面部区域替换为 GT 面部，仅评估非人脸区域的质量。Table 3 显示，Face2Scene 在此设定下仍以 8/10 的指标优势超越 S3Diff，证明 FaDeX 提取的退化信息成功通过 MapNet 传递到整个人物场景，而非仅作用于面部附近区域。

**退化表示的语义解耦。** Figure 4 通过余弦相似度分析验证了 FaDeX 嵌入的退化-内容解耦能力。对于相同退化类型、不同图像内容的样本对，FaDeX 嵌入保持高相似性；对于不同退化类型，相似度则显著降低。这一模式在“按退化类型平均”和“按图像平均”两个视角下均成立，阴影区域显示标准差较小，表明解耦行为稳定。

### 失败模式与局限性

尽管 Face2Scene 在全局一致退化场景下表现优异，其核心假设——退化在整幅图像中空间一致——构成了主要局限。对于包含局部变化退化的场景（如运动模糊仅在移动主体上出现、景深效果导致前景/背景模糊程度不同），统一的退化代码无法准确描述全局退化分布，可能导致部分区域恢复不足或过度锐化。此外，该方法依赖现成参考面部修复模型的输出质量：若面部重建不准，FaDeX 将提取到错误的退化信息，并通过 MapNet 传播到全图。同时，身份参考图像的需求限制了其在无参考场景下的直接应用。

### 开放问题

如何将 Face2Scene 的退化感知框架扩展到空间变化退化场景（如景深模糊、运动模糊），是值得进一步探索的方向。可能的路径包括从多个人脸区域或显著性区域分别提取局部退化代码，或设计空间自适应的退化令牌注入机制。

![[assets/figures/papers/paper_list_l2483_https_openaccess_thecvf_com_content_CVPR2026_html_Kazerouni_Face2Scene_U/figures/006_Table_2.jpg]]
*Table 2: Quantitative comparison on the InScene synthetic and real validation sets. Arrows indicate whether lower (↓) or higher (↑) values are better. Here, 1+N denotes a single diffusion step plus N additional inference steps of a Ref-FR model. C-IQA and M-IQA denote CLIP-IQA and MANIQA, respectively. Each cell is color-coded to represent the best and second-best performance*

![[assets/figures/papers/paper_list_l2483_https_openaccess_thecvf_com_content_CVPR2026_html_Kazerouni_Face2Scene_U/figures/007_Table_3.jpg]]
*Table 3: Scene and face restoration analysis. “GT Face Inserted” indicates we composite the ground-truth face region into the restored image to isolate each method’s impact on the rest of the scene. The two rows (“Face only”) report metrics computed only within the facial region (without GT insertion). LIQE for face only is not reported because the model is sensitive to input size and cannot handle small face sizes. The last two rows show our method with and without the proposed degradation estimation. The best value per metric is bolded*

![[assets/figures/papers/paper_list_l2483_https_openaccess_thecvf_com_content_CVPR2026_html_Kazerouni_Face2Scene_U/figures/004_Figure_3.jpg]]
*Figure 3: Visual comparison of Face2Scene with the three top-performing methods from the quantitative results (zoom in to see details)*

## 定位与知识库关联

### 1. 与现有工作的关系

Face2Scene 的核心贡献在于将**退化估计**从“盲猜”转变为“以面部为先知”的确定性推理，从而在退化感知扩散恢复这一脉络中开辟了新的技术路线。我们将其置于以下方法谱系中进行分析。

#### 1.1 通用盲复原方法

**Real-ESRGAN** 和 **DiffBIR** 代表了两种主流的盲复原范式：前者通过纯合成数据训练 GAN 实现通用盲复原，后者将扩散模型引入退化去除流程。两者的共同瓶颈在于**缺乏显式的退化建模**——它们试图从单张低质量图像中隐式学习退化到清洁图像的映射。这种“端到端盲映射”在退化类型与训练分布一致时表现尚可，但在真实场景中退化复杂多变时，问题高度欠定，容易产生过度平滑或伪影。

Face2Scene 与这类方法的本质区别在于：它不试图从单张 LQ 图像中盲猜退化，而是**利用同一身份的高质量参考面部作为“退化测量仪”**，通过 LQ-HQ 面部对的对比，精确推断出当前图像的退化类型与强度。这使得退化估计问题从“欠定推断”转变为“有条件测量”，从根本上降低了不确定性。

#### 1.2 退化引导的扩散复原方法

**S3Diff** 是目前与 Face2Scene 最接近的工作，它首次尝试将退化信息显式注入一步扩散模型。然而，S3Diff 的退化表示仅为**两个全局标量**（噪声水平和模糊核宽度），通过调制 LoRA 权重来影响生成过程。这种低维表示的信息容量极为有限，无法刻画真实世界中复杂的退化组合（如噪声+模糊+压缩的叠加效应），且全局标量假设退化在空间上均匀分布，忽略了局部变化。

Face2Scene 在此基础上进行了两个关键升级：
- **退化表示维度**：从 2 个全局标量升级为 **21 个多尺度空间感知令牌**（通过 MapNet 的 4×4、2×2、1×1 网格平均池化生成），能够编码更丰富的退化上下文；
- **退化注入机制**：从 LoRA 权重调制改为**交叉注意力注入**，使退化令牌能够与 SD-Turbo 的中间特征进行更灵活的信息交互。

消融实验（Table 3）直接验证了这一升级的有效性：在修复图像中插入真实人脸以隔离非人脸区域后，Face2Scene 在 10 项指标中赢得 8 项，表明退化信息成功从面部传递到整个人物场景，而 S3Diff 的全局标量无法实现这种跨区域的退化指导。

#### 1.3 退化编码学习范式

**DeeDSR** 采用无监督对比学习来学习退化表示，其核心思路与 FaDeX 的对比损失有相似之处。但 DeeDSR 的退化编码仍从单张图像中提取，面临内容与退化纠缠的挑战。Face2Scene 的关键创新在于**利用 LQ-HQ 面部对作为对比信号源**：FaDeX 接收拼接的 LQ 和 HQ 面部作为输入，通过对比损失强制相同退化算子的嵌入相互吸引、不同退化的相互排斥。Figure 4 的余弦相似度分析证实，FaDeX 嵌入在不同图像内容间对相同退化保持高度一致，而对不同退化相似度极低，证明其成功解耦了退化与内容——这一特性是单图退化编码方法难以保证的。

#### 1.4 人体感知的场景恢复

**HAODiff** 聚焦于人体区域的感知质量增强，使用一步扩散模型进行场景恢复。Face2Scene 与之共享一步扩散的高效推理优势，但差异在于：HAODiff 缺乏显式退化估计，而 Face2Scene 通过面部退化代码为扩散模型提供了精确的“去退化”目标。这种退化感知能力使 Face2Scene 在处理严重退化场景时具有更强的鲁棒性。

### 2. 适用边界与局限

#### 2.1 核心假设：空间一致退化

Face2Scene 的方法设计隐含假设**退化在整幅图像中是空间一致的**。FaDeX 从面部区域提取的退化代码被 MapNet 转化为全局条件令牌，注入扩散模型后作用于整个场景。这一假设在全局噪声、均匀模糊、压缩伪影等场景下成立，但在以下情况中会失效：
- **景深模糊**：前景清晰、背景模糊的摄影效果；
- **运动模糊**：仅出现在运动物体上的局部模糊；
- **局部光照退化**：仅影响部分区域的过曝或欠曝。

在这些场景中，面部区域的退化类型可能与非人脸区域不同，导致退化估计产生系统性偏差。论文未提供针对空间变化退化的实验验证，这一局限需要在实际部署时审慎评估。

#### 2.2 对参考面部修复模型的依赖

Face2Scene 的性能链式依赖于现成的参考面部修复模型（off-the-shelf Ref-FR）的输出质量。如果 Ref-FR 模型在极端退化下无法准确重建面部，FaDeX 将从一个错误的 HQ-LQ 对中提取退化代码，进而导致全场景恢复失败。此外，该方法**需要身份参考图像**，这限制了其在无参考场景（如监控视频中的陌生人）中的应用。虽然论文未明确讨论 Ref-FR 模型的鲁棒性边界，但这一依赖关系意味着 Face2Scene 的下限由所选 Ref-FR 模型决定。

#### 2.3 训练数据与泛化边界

根据 Table 1，训练集包含 57,449 张图像（来自 1,819 个身份），其中合成数据 11,266 张。合成退化类型的具体组合未在分析中详细说明，但可以推断模型的泛化能力受限于训练时见过的退化分布。对于训练分布外的退化类型（如特定相机的传感器噪声模式、非高斯模糊核），退化估计的准确性需要手动验证。

### 3. 开放问题

1. **空间变化退化的建模**：如何扩展 FaDeX 以提取空间感知的退化图（degradation map），而非全局退化代码？一个可能的方向是将面部区域划分为多个子块，分别估计局部退化，再通过空间插值生成全图退化场。

2. **无参考场景的退化估计**：当身份参考图像不可用时，能否从单张 LQ 面部中直接估计退化？这需要探索退化与内容的解耦表示学习，可能结合预训练的面部先验模型。

3. **退化代码的可解释性与可控性**：FaDeX 学习到的 21 个多尺度令牌是否对应可解释的退化属性（如噪声强度、模糊半径、压缩质量因子）？如果能实现退化维度的解耦，用户将能够交互式地调整恢复程度。

4. **多面部融合策略**：当场景中存在多个人物时，不同面部可能经历略有不同的退化（如距离相机远近不同导致的尺度差异）。如何融合多个面部退化代码以获得更准确的全局退化估计，是一个尚未探索的问题。

## 原文 PDF

![[paperPDFs/CVPR_2026/Face2Scene_Using_Facial_Degradation_as_an_Oracle_for_Diffusion_Based_Scene_Restoration.pdf]]

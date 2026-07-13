---
title: "Adapting Self-Supervised Representations as a Latent Space for Efficient Generation"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Adapting_Self_Supervised_Representations_as_a_Latent_Space_for_Efficient_Generation.pdf
project_link: null
code_link: https://github.com/CompVis/RepTok
aliases:
- RTR
- ASSRALSEG
tags:
- ICLR_2026
- topic/generative_models_diffusion
- topic/generative_models_diffusion/generative_models_and_autoencoders
core_operator: "仅微调预训练SSL视觉Transformer的[cls]令牌嵌入，同时应用余弦相似度正则化项，使单个连续令牌既能注入重建所需的底层细节，又保留原SSL空间的平滑几何结构。"
primary_logic: "预训练自监督模型的池化[cls]向量本身构成一个平滑、语义结构良好的连续潜在空间；只需最小适配（微调[cls] token + 余弦相似度约束）即可直接作为生成模型的潜在空间，彻底消除2D空间冗余，大幅降低训练成本。"
claims:
- "RepTok仅用1个连续令牌即达到重建rFID 1.85、生成gFID 1.88，与31～256个令牌的现有方法竞争。"
- "微调[cls]令牌能显著提升重建质量，相比冻结状态恢复了精细细节。"
- "余弦相似度损失权重λ可控制重建-生成权衡：低λ增强像素级重建（高PSNR）但生成极差（高gFID），高λ则相反。"
- "潜在空间插值在语义和空间布局上均呈现平滑过渡，证明潜在空间兼具低层空间信息。"
---

# Adapting Self-Supervised Representations as a Latent Space for Efficient Generation

> [!tip] 核心洞察
> 预训练自监督模型的池化[cls]向量本身构成一个平滑、语义结构良好的连续潜在空间；只需最小适配（微调[cls] token + 余弦相似度约束）即可直接作为生成模型的潜在空间，彻底消除2D空间冗余，大幅降低训练成本。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 自适应自监督表征作为高效生成的潜在空间 |
| 英文题名 | Adapting Self-Supervised Representations as a Latent Space for Efficient Generation |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=0b6a2SE23v) · [GitHub](https://github.com/CompVis/RepTok) |
| Topic | #topic/generative_models_diffusion #topic/generative_models_diffusion/generative_models_and_autoencoders |
| Method | Representation Tokenizer (RepTok) |
| Dataset | ImageNet 256×256, ImageNet 256×256 类别条件生成 (无CFG), MS-COCO zero-shot |

> [!tip] 效果简介
> - ImageNet 256×256 上，gFID 为 1.88，对比 LDM: 7.76, TiTok-B: 2.48, FlexTok d18-d28: 1.86，变化 与最强基线FlexTok (1.86) 相当，但令牌数量少两个数量级。
> - ImageNet 256×256 上，rFID 为 1.85，对比 LDM: 0.90, TiTok-L: 2.21, FlexTok d12-d12: 4.20，变化 优于TiTok-L (2.21) 和FlexTok (4.20)，接近基于大网格的LDM (0.90)。
> - ImageNet 256×256 类别条件生成 (无CFG) 上，FID 为 5.4 (Stage2 100K步)，对比 DiT-XL/2: 19.5 (7M步), SiT-XL/2: 17.2 (7M步)，变化 仅需1/70的训练步数，FID大幅领先。

## 概要

现有潜在扩散模型大多将图像编码为二维网格潜在表示，或通过多令牌（如32个离散令牌）序列压缩，但这些表示仍存在显著空间冗余，且训练与推理计算开销巨大。RepTok 提出一种极简范式：仅用一个连续令牌来表征图像，该令牌直接从预训练自监督视觉 Transformer 的 `[cls]` 嵌入获得。

核心思路是**微调自监督编码器的 `[cls]` 令牌嵌入，同时施加余弦相似度正则化，既注入重建所需的底层细节，又保持自监督潜在空间的平滑语义结构**。由此，一个紧凑且几何性质良好的连续潜在空间便可直接用于图像重建与生成，无需传统二维网格或码本量化。

在 ImageNet 256×256 上，RepTok 以单个连续令牌实现重建 rFID 1.85、生成 gFID 1.88，与使用 31～256 个令牌的同类方法相当，但令牌数量减少了一到两个数量级。类别条件生成仅需少量训练（Stage 2 仅 100K 步）即达到 FID 5.4，显著优于需要百万步训练的 DiT/SiT 基线，训练成本降低超 90%。潜在空间插值在语义和空间布局上均呈现平滑过渡，表明单令牌表示成功整合了低层空间信息。RepTok 的生成模型甚至可基于纯 MLP 架构（MLP-Mixer），推理耗时仅 0.27 秒，整体推理速度优于基于注意力的扩散 transformer。



当前主流的视觉生成模型大多在二维网格化的潜在空间上构建。以潜在扩散模型（LDM）为代表，图像首先被压缩为低维特征图（如 16×16 或 32×32），生成器再对该空间中的网格型潜变量进行建模。这类二维布局固然保留了部分空间结构，却也带来了大量的空间冗余：相邻位置携带的信息高度相似，但生成模型仍然必须对所有网格元素进行完整的一步或迭代预测。即便后续工作尝试将图像表示为更紧凑的一维序列（例如 TiTok 用 32 个离散令牌，FlexTok 用可变长度的连续令牌），每个样本依然需要数十个令牌才能兼顾重建与生成质量。训练这种多令牌潜空间上的扩散或流匹配模型，需要极大的计算开销——典型的 DiT‑XL/2 或 SiT‑XL/2 需要数百万甚至上千万训练步，其训练 FLOPs 高达数千 TFLOPs，这严重限制了快速实验与资源受限场景下的应用。

与此同时，自监督视觉 Transformer（如 DINOv2）在大量无标签数据上学习到的表征，其 [cls] 汇聚输出本身便是一个高度浓缩的连续向量，天然具有平滑且语义结构良好的几何特性。已有的尝试（如 RCG）直接冻结这类编码器并将其输出作为生成模型的条件，但由于没有向潜码注入重建所需的底层细节，重建质量较差（rFID 3.20，PSNR 9.31 dB），生成的图像也无法刻画精细结构。这一矛盾提示：若能在几乎不改变自监督空间几何的前提下，让 [cls] 令牌额外携带适度的空间线索，就有望将图像压缩至极致的单个连续令牌，同时消灭 2D 网格与多令牌带来的冗余，进而允许生成模型在维度极低的潜在空间上高效学习。

这正是本工作的核心动机——探索如何将预训练自监督表征直接转化为高效生成所需的最小化潜在空间。研究者观察到，只需对 [cls] 令牌的嵌入进行定向微调，并施加一个余弦相似度损失以约束其方向不偏离冻结编码器输出的原始方向，即可在单个连续令牌中同时保留语义光滑性与注入的低层重建信息。这一发现意味着，生成该潜空间的第二阶段模型只需学习一维连续分布，不再需要处理空间结构上复杂的交互。最终，RepTok 实现在 **单一连续令牌** 下取得 rFID 1.85、gFID 1.88 的重建与生成指标，与使用 31～256 个令牌的现有先进方法竞争（Table 1）；与之配套的轻量生成器（如纯 MLP‑Mixer）仅需同类 Transformer 基线 1/70 的训练步数即可达到更优的类别条件生成 FID（Table 2），总训练 FLOPs 降低超过 90%（Figure 1）。这一大幅压缩的潜在空间也为快速原型化新的生成架构和扩展现有多模态模型提供了全新视角。



## 核心方法与创新机理

现有潜在生成模型普遍依赖高维度的空间离散表征：LDM 将图像压缩为二维网格型潜变量，TiTok 等则使用多枚离散令牌（如 32 个）。这类设计包含大量空间冗余，即使压缩到极少数令牌仍无法达到彻底的紧凑性，同时加剧本已高昂的训练与推理开销。RepTok 的核心洞见在于：**预训练自监督 ViTs 的池化 `[cls]` 向量本身即构成一个平滑、语义结构良好的连续潜在空间**，只需极小的适配就能直接作为生成模型的潜变量，从而完全消除二维空间冗余。据此，工作围绕三个相互咬合的“变动的槽位”（changed slots）构建起轻量生成范式：

1. **极端压缩的潜在令牌数量**  
   将潜变量从 TiTok 的 32 个离散令牌或 LDM 的 16×16 网格压缩为 **单个连续令牌**（`evidence_anchor: "a single continuous latent token"`）。该令牌直接取自冻结 SSL 编码器的 `[cls]` 输出，不再需要离散码本或空间网格。此举使潜变量的维度从 256×（如 32×32）降至 1×768，彻底移除空间结构，极大削减后续生成模型的计算负担。

2. **稀疏化的编码器微调策略**  
   区别于 RCG 等完全冻结编码器的做法，RepTok **仅微调 `[cls]` 令牌嵌入，其余所有参数保持冻结**（`evidence_anchor: "only updates the class token embedding while keeping the remainder of the encoder frozen"`）。这一策略的因果机理是：冻结的编码器保留了自监督预训练空间的平滑几何与语义一致性，而微调后的 `[cls]` 令牌能够在保持原有空间方向的前提下，额外吸收重建所需的底层细节（纹理、空间结构）。消融实验（Figure 5）直观显示，微调后的潜变量能恢复大量被冻结条件完全丢失的精细细节，证明单一的 `[cls]` 向量足以携带丰富且必要的重建信息。

3. **几何保持的正则化损失**  
   为防止微调破坏预训练空间的优良性质，引入**余弦相似度损失**  
   $$ \mathcal{L}_{\text{cos}}(x) = \lambda \,(1 - \cos(z, z_{\text{frozen}})) $$  
   该损失约束微调后的 `[cls]` 令牌与冻结编码器输出保持方向一致（`evidence_anchor: "preserve the beneficial properties of the pre-trained space"`）。此正则化项的权重 λ 形成了一个可调节的“重建‑生成权衡”：λ→0 时，像素重建质量（PSNR）达到最高，但生成质量急剧恶化（gFID 极差）；λ 增大则 gFID 改善而 PSNR 有所下降（Figure 9）。正是这种几何约束，使得后续的生成模型可以仅在一个紧凑、有序的连续潜空间中进行建模，而无需额外的辅助损失或复杂的表示对齐。

上述三个槽位通过管道中的四个模块协同实现（Figure 2）：**① 预训练 SSL 编码器**（冻结主体，仅 `[cls]` 令牌可学习）负责将图像映射为单个潜令牌 $z$；**② 余弦相似度损失模块**在微调过程中维持潜空间的方向一致性；**③ 生成式解码器 $D$**（DiT‑XL/2，以流匹配训练）以 $z$ 为条件将噪声还原为图像（在预训练 VAE 潜空间内操作），实现高质量重建；**④ 潜在空间生成模型 $G$**（MLP‑Mixer 或 Transformer，流匹配训练）对冻结编码器输出的潜分布进行建模，支持类别/文本条件采样。值得注意的是，由于潜空间已具备良好结构，第二阶段生成模型甚至可采用无注意力的纯 MLP 架构（MLP‑Mixer），其生成耗时仅 0.27 s，远小于解码器的 0.95 s（Table 5），总推理时间比 DiT‑XL/2 更短。

### 证据与权衡

- **重建与生成质量**：RepTok 仅用 1 个连续令牌即实现重建 rFID 1.85、生成 gFID 1.88（Table 1），达到与 31～256 个令牌的 FlexTok、TiTok 等模型相当甚至更优的性能。在类别条件 ImageNet 生成中，第二阶段仅训练 100K 步（约 1/70 的基线训练量）即获得 FID 5.4（无 CFG），大幅超越需训练 7M 步的 DiT‑XL/2（FID 19.5）和 SiT‑XL/2（FID 17.2）（Table 2）。
- **潜空间平滑性**：潜在插值实验（Figure 4）表明，潜空间不仅在语义内容上，还在空间布局上呈现平滑过渡，验证了所提方法成功将底层空间信息注入潜向量并保持 SSL 空间的几何性质。
- **组件重要性**：若使用寄存器令牌（register token）虽能获得更高的 PSNR（12.85 vs. 12.59），但其空间未受 SSL 正则化约束，不利于后续生成（Table 6）。随机初始化的编码器虽可取得尚可的像素重建，但潜空间完全无序，无法产生合理的生成样本（Figure S9、Table 4），进一步证明了依赖预训练 SSL 空间并加以几何保持的必要性。
- **固有局限**：λ 所控制的忠实度‑生成度权衡意味着，在追求极高像素重建保真度的任务中，模型必须牺牲生成质量，反之亦然。此外，极致的单令牌压缩虽然成就了效率突破，也可能限制对多对象精确定位或复杂场景的细粒度控制（该方法尚未对此提供解决方案）。这些取舍指出了未来可能在单令牌空间的表达能力扩展与条件调控方面的发展方向。



![[assets/figures/papers/iclr26_0006_0b6a2SE23v_Adapting_Self-Supervised_Representations_as_a_La/figures/004_Figure_2.jpg]]
*Figure 2: Overview of our pipeline. (a) Joint fine-tuning of the [cls] token of SSL encoder E and training of the generative decoder D for image reconstruction. (b) Training of the generation model G to synthesize frozen encoder outputs, which constitute the latent space z = E(x). (c) Inference pipeline, where the latent space z is first generated and subsequently decoded into the pixel space*

RepTok 将图像映射为单个连续潜在令牌，并直接在该令牌构建的一维连续空间上执行生成建模。整个框架的核心思路是利用预训练自监督视觉 Transformer 的 [cls] 池化向量作为紧凑、语义结构良好的表示基础，再通过极轻量的适配注入重建所需的底层信息，从而彻底消解传统二维网格潜在空间中的空间冗余。

整体流水线如图 2 所示，由两个训练阶段和一个推理阶段组成：

1. **第一阶段：编码器-解码器联合训练（图 2a）**
   - **预训练 SSL 编码器** 以冻结状态接收图像 $x$，但将其 [cls] 令牌对应的嵌入设置为可训练参数，其余参数完全冻结。编码器输出单个连续潜在令牌 $z \in \mathbb{R}^{1 \times 768}$。
   - **余弦相似度正则化** 计算 $\mathcal{L}_{\mathrm{cos}} = \lambda (1 - \cos(z, z_{\mathrm{frozen}}))$，约束微调后的 $z$ 与冻结编码器输出的方向一致，保护预训练空间的平滑几何结构。
   - **生成式解码器** 以 $z$ 为条件，通过流匹配学习从标准高斯噪声到目标图像（在预训练 VAE 潜空间内）的向量场。解码器采用 DiT‑XL/2 架构，将 $z$ 与补丁令牌拼接后进行完整自注意力运算，训练目标为 $\mathcal{L} = \mathbb{E}_{t, x_0, x_1} \| v_\theta(t, x_t, z) - (x_1 - x_0) \|$。
   - 该阶段总损失为流匹配重建损失与余弦相似度对齐损失之和，仅更新 [cls] 令牌嵌入和解码器参数。此举在维持 SSL 空间优质性质的同时，令单个令牌承载重建所需的精细局部信息。

2. **第二阶段：潜在空间生成模型训练（图 2b）**
   - 固定训练好的编码器（冻结 [cls] 令牌），对所有训练图像提取潜在令牌 $z$，构成紧凑的一维连续潜在空间。
   - 在该空间上训练**潜在空间生成模型** $G$，同样使用流匹配目标，$\mathcal{L} = \mathbb{E}_{t, z_0, z_1} \| v_\theta(z_t, t) - (z_1 - z_0) \|$，并支持类别或文本条件注入。
   - 得益于潜在空间的高紧凑性和良好性质，生成模型可采用纯 MLP 的 MLP‑Mixer 架构，无需注意力机制，也不依赖辅助损失。

3. **推理流程（图 2c）**
   - 从噪声采样 $z_1$，经 $G$ 逆向流映射获得合成潜在令牌 $z_0$。
   - 解码器 $D$ 以 $z_0$ 为条件执行逆向流匹配（或采用常微分方程采样），重建出最终图像。
   - 两阶段解耦使推理时只需运行轻量 MLP‑Mixer 与一次解码，总耗时约 1.22 秒（其中 MLP‑Mixer 仅 0.27 秒）。

整个设计将“表示学习”与“分布建模”彻底解耦：编码器只负责将图像压缩为一个连续令牌，生成模型仅需拟合一个极低维（768 维）的平滑分布，从而以仅 1 个令牌的数量级差距，在重建和生成指标上与使用 32~256 个令牌的方法相竞争（rFID 1.85, gFID 1.88，表 1）。



RepTok 的整体管线分为两个阶段（Figure 2）：(i) **自适应编码与重建**——冻结 SSL 编码器的大部分参数，仅微调 `[cls]` 令牌嵌入，同时以流匹配训练一个生成式解码器，并加入余弦相似度正则化，使单个连续潜在令牌既能注入重建所需的底层细节，又保留原 SSL 空间的平滑几何；(ii) **潜在空间生成建模**——固定编码器，将 `[cls]` 令牌视为潜变量，用一个轻量生成模型建模其分布，实现高效的图像合成。以下逐一剖析各关键模块及其公式。

### 1. 自适应 SSL 编码器 $\mathcal{E}$

$\mathcal{E}$ 是一个预训练的 SSL 视觉 Transformer（如 DINOv2），将输入图像 $x$ 映射为一个 $d=768$ 维的 `[cls]` 令牌嵌入：
$$
z = \mathcal{E}(x)
$$
为弥合 SSL 预训练目标与像素级重建之间的鸿沟，我们实施**针对性适配（targeted adaptation）**：仅更新 `[cls]` 令牌嵌入，其余编码器权重全部冻结。这一极小的参数改动便能让 $z$ 含纳重建所需的精细纹理与空间信息，而原骨干的语义结构几乎不受破坏。

### 2. 流匹配解码器 $\mathcal{D}$ 与重建损失

解码器 $\mathcal{D}$ 采用 DiT‑XL/2 架构（配备 RoPE、RMSNorm 与 SwiGLU），在预训练的 SD‑VAE 潜空间内工作。它以 `[cls]` 令牌 $z$ 为条件，学习从标准高斯噪声 $x_0$ 到目标潜变量 $x_1$ 的向量场 $v_\theta$。重构训练最小化以下流匹配期望损失：

$$
\mathcal{L}_{\text{dec}}(x) = \mathbb{E}_{t,\,x_0,\,x_1}
\Big\| v_\theta\big(t,\,x_t,\,z\big) -
\big(x_1 - x_0\big) \Big\|
\qquad\text{(Equation (2))}
$$
其中，
- $t \in [0,1]$ 为流动时间；
- $x_t = t\,x_1 + (1-t)\,x_0$ 是线性插值路径；
- $x_0 \sim \mathcal{N}(0,I)$，$x_1$ 为由图像经 VAE 编码得到的真实潜变量；
- $z$ 为编码器输出的单令牌表示。

实现中，$z$ 与解码器的 patch 令牌拼接后参与全自注意力运算，使单令牌条件信号能够影响所有层的空间重建。该损失端到端地将单令牌编码与像素保真度耦合在一起。

### 3. 余弦相似度正则化项

若不加约束直接微调，`[cls]` 令牌的方向可能偏离原 SSL 空间，破坏其平滑且语义良好的几何特性，从而削弱后续生成。为此引入方向性正则：

$$
\mathcal{L}_{\text{cos}}(x) = \lambda \big(1 - \cos(z,\,z_{\text{frozen}})\big),
\qquad
z_{\text{frozen}} = \mathcal{E}_{\text{frozen}}(x)
\qquad\text{(Equation (3))}
$$
其中，
- $\mathcal{E}_{\text{frozen}}$ 是完全冻结的编码器副本；
- $\cos(\cdot,\cdot)$ 为余弦相似度；
- $\lambda$ 是控制正则化强度的重要超参数。

该项惩罚 $z$ 与冻结版本 $z_{\text{frozen}}$ 之间的方向偏差，迫使自适应令牌保持与原 SSL 空间近似共线。$\lambda$ 实质调节**重建‑生成权衡**：低 $\lambda$ 得到高 PSNR 但生成发散（gFID 恶化），高 $\lambda$ 则生成质量提升但像素还原能力下降（Figure 9）。实证发现 $\lambda=0.1$ 在 ImageNet 上取得优良平衡。

### 4. 潜在空间生成模型 $\mathcal{G}$

Stage 2 完全冻结编码器 $\mathcal{E}$，将得到的 $z$ 视为一个紧凑的 $768$ 维连续隐变量，在其分布上训练生成模型 $\mathcal{G}$。$\mathcal{G}$ 同样基于流匹配，通过向量场 $v_\phi$ 将高斯噪声“输送”到真实数据分布。其训练目标与式 (1) 同构，但作用于潜在令牌空间：

$$
\mathcal{L}_{\text{gen}} = \mathbb{E}_{t,\,z_0,\,z_1}
\big\| v_\phi(z_t,\,t) - (z_1 - z_0) \big\|
$$
其中 $z_0 \sim \mathcal{N}(0,I)$ 为噪声，$z_1$ 是经冻结 $\mathcal{E}$ 抽取的真实 1D 潜在令牌，$z_t = t\,z_1 + (1-t)\,z_0$。

对于类别条件生成，我们采用**MLP‑Mixer**（隐藏维 1280、深度 28、通道/令牌 MLP 扩展因子分别为 4 和 2）作为 $\mathcal{G}$，将类别标签注入后直接沿着时间维度进行流匹配。实验表明，无注意力的纯 MLP 架构即可有效捕捉该平滑连续空间的分布，且推理延时可忽略（0.27 s vs. 解码器的 0.95 s；Table 5）。生成阶段的计算开销因此大幅削减，结合单令牌紧凑表示，最终使总训练成本较 DiT‑XL/2 降低超过 90 %（Figure 1，Table 2）。



## 实验与关键发现

### 主结果：单令牌紧凑重建与高效生成

**ImageNet 256×256 重建与生成（Table 1）**  
RepTok 仅用 **1 个连续令牌**（[cls] 向量）即达到令人意外的紧凑表达能力：重建 rFID **1.85**，生成 gFID **1.88**，其 gFID 与使用 18～28 个可变长度令牌的 FlexTok（1.86）基本持平，且显著优于 32 枚离散令牌的 TiTok‑B（2.48）和基于 16×16 网格的 LDM（7.76）。在重建指标上，RepTok 的 rFID 亦明显优于 TiTok‑L（2.21）和 FlexTok（4.20），接近需要大量空间冗余的 2D 网格方法 LDM（0.90）。这表明 **1 个连续的 SSL 池化向量足以替代整个 2D 网格潜在空间，彻底消除空间冗余**。


![[assets/figures/papers/iclr26_0006_0b6a2SE23v_Adapting_Self-Supervised_Representations_as_a_La/figures/008_Table_1.jpg]]
*Table 1: State-of-the-art comparison between tokenizers for reconstruction and class-conditional ImageNet generation. † metrics sourced from (Bachmann et al., 2025)*

**类别条件生成与训练成本（Table 2、Figure 1）**  
在 ImageNet 256×256 类别条件生成中，RepTok 的 Stage2 仅用 **100K 训练步**即达到无分类器引导（CFG）的 FID **5.4**，远优于训练步数高出一个数量级的 DiT‑XL/2（7M 步，FID 19.5）和 SiT‑XL/2（7M 步，FID 17.2）。引入 CFG=1.5 后，FID 进一步降至 **3.22**（700K 步），继续领先同类轻量基线。训练开销的对比更为直观：SiT‑B/2 的编码器与生成模型合计约需 240 GFLOPs，而 RepTok 的编码器仅约 40 GFLOPs（降低 83.1%），生成模块仅约 20 GFLOPs（降低 91.7%，Figure 1）。这些 FLOPs 估算已排除共享的 SD‑VAE 和 DINOv2 预训练成本，公平反映了差异化的训练开销。


![[assets/figures/papers/iclr26_0006_0b6a2SE23v_Adapting_Self-Supervised_Representations_as_a_La/figures/009_Table_2.jpg]]
*Table 2: FID comparison on the ImageNet 256 × 256 benchmark, including parameter counts and training FLOPs. Stage 1 refers to the training of the generative decoder, while Stage 2 corresponds to the main generative model training. As all models rely on the SD-VAE and REPA uses DINOv2 as well, we exclude these shared pre-training costs from FLOP estimates*

![[assets/figures/papers/iclr26_0006_0b6a2SE23v_Adapting_Self-Supervised_Representations_as_a_La/figures/003_Figure_1.jpg]]
*Figure 1: Comparison of our single-token MLP-Mixer generator against transformer-based baselines (DiT, SiT), as well as representation-aligned models like REPA. RepTok attains competitive generative performance while reducing training cost by over 90% owing to its compact latent space and lightweight architecture. All results reported without CFG. For fair comparison, we employ an encoder and decoder trained on general-domain data*

**Text‑to‑Image 零样本生成（Figure 7）**  
在 MS‑COCO 零样本设置下，以冻结的 Gemma 2.5B 为语言骨干时，RepTok 的 **FID‑5k 约 41**，与基于 Transformer 的 MicroDiT 相当，而训练耗时不足 20 小时（前者需数天）。进一步更换骨干为 CLIP 或 InternVL3 时，FID‑5k 随骨干规模提升而降低（CLIP~51，InternVL3~46），说明方法可有效受益于更大规模的语言模型，同时保持训练效率。

**与冻结表征生成方法的对比（Table 3）**  
与同样利用冻结 SSL 表征的 RCG 相比，RepTok 的重建质量大幅度领先：FID@50K **1.85 vs 3.20**，PSNR **14.94 vs 9.31**。这归因于对 [cls] 令牌的定向微调和流匹配解码器的联合训练，使单一令牌能注入必要的底层信息。

### 消融分析

**微调 [cls] 令牌的原因（Figure 5）**  
冻结整个 SSL 编码器时，重建图像丢失大量纹理、边缘等精细细节；仅微调 [cls] 令牌的嵌入即可显著恢复这些底层信息。这一最小化改动（仅更新约 $768$ 维参数）在保持编码器其余部分不变的情况下，使 rFID 从极高降至 **1.85**，印证了单令牌适配的充分性。


![[assets/figures/papers/iclr26_0006_0b6a2SE23v_Adapting_Self-Supervised_Representations_as_a_La/figures/007_Figure_5.jpg]]
*Figure 5: Fine-tuning the [cls] token. From left: GT, frozen, finetuned*

**令牌类型的影响（Table 6、Figure S7）**  
对比 DINOv2 的寄存器（register）令牌与 [cls] 令牌，寄存器令牌因携带更多局部信息，其重建 PSNR 略优（12.85 vs 12.59）且 SSIM 更高（29.07 vs 28.41）。但寄存器令牌并未受益于 SSL 的余弦相似度正则化，其生成质量大幅下降；增加寄存器令牌数量虽能提升重建，却会破坏潜在空间的平滑性，导致生成样本失控。因此，**预训练 SSL 空间的结构化特性是良好生成的关键**。

**余弦相似度正则化的权衡（Figure 9）**  
控制余弦损失权重 $\lambda$ 可调节重建‑生成之间的平衡：低 $\lambda$（如 $\lambda=0$ 至 $10^{-3}$）释放了更强的像素级重建能力（PSNR 约 14.5～15），但 gFID 极差（≈65），几乎退化为纯重建任务；高 $\lambda$（如 $\lambda=0.1$）则使 gFID 达到最优（≈1.88）而 PSNR 降至约 13.2。该曲线明确展示了正则化项在保留 SSL 空间几何特性与注入重建细节之间的核心矛盾。


![[assets/figures/papers/iclr26_0006_0b6a2SE23v_Adapting_Self-Supervised_Representations_as_a_La/figures/017_Figure_9.jpg]]
*Figure 9: The parameter λ of the cosine similarity loss in Equation (3) allows us to trade off between pixel-wise reconstruction and generation capabilities. Relaxed constraints (low λ) improve pixel-wise reconstruction (PSNR in right plot), but result in poor generation capabilities (gFID in right plot)*

**预训练 SSL 的必要性（Table 4、Figure S9）**  
若使用随机初始化的编码器替代预训练 SSL 骨干，尽管在 10K 步即可获得较高的像素重建指标，但其潜在空间完全无序，导致类别条件生成样本几乎无意义（类似随机噪声）。这一对比直接证明 **SSL 预训练赋予的平滑、语义有序的潜在空间是生成能力的根基**，而定向适配仅需保留并微调该空间的少量参数（对比见 Table 4，各种 SSL 编码器 DINOv2、MAE、CLIP 均可工作，但随机初始化失败）。

**生成模型架构的轻量性（Table 5、Figure 10）**  
潜在空间的生成模型采用 **注意力自由的 MLP‑Mixer**，其推理耗时仅 **0.27 s**，远小于解码器的 0.95 s，总推理时间 1.22 s，仍优于重量级扩散 Transformer（如 DiT‑XL/2）。MLP‑Mixer 还表现出良好的参数缩放行为：从约 20M 参数的 S 版本到 516M 的 XL 版本，生成性能持续提升（Figure 10），为高效部署提供了灵活的选择。

### 潜在空间性质与生成平滑性

**潜在空间插值的语义‑空间协同（Figure 4）**  
在潜在空间中对两个图像的 [cls] 令牌进行线性插值，解码后图像呈现出语义类别与空间布局的**双重平滑过渡**（如从“雪中建筑”逐渐变为“绿植覆盖的山丘”）。这证实单令牌在保留高层语义的同时，也编码了足够的空间配置信息，这正是余弦相似度正则化通过保持与冻结表征方向对齐所带来的结构优势。

### 失败模式与内在限制

尽管 RepTok 实现了极低的令牌数量与显著的训练效率，其设计引入了几项内在权衡：

- **重建‑生成折中不可消除**：余弦相似度损失强制潜在令牌保持与冻结 SSL 空间的方向一致，导致高保真重建（需要偏离原空间）与高质量生成（需要空间平滑）永远是一对矛盾体。λ 的调节只能在两端之间选择平衡点，无法同时取得最优。
- **预训练依赖与分布限制**：方法完全依赖于预训练 SSL 编码器的潜在空间结构，若预训练数据分布与下游生成目标存在较大偏差，冻结空间的语义对齐可能失效，且固定编码器无法通过训练适应新数据。
- **多令牌扩展的生成代价**：虽然增加寄存器等非 SSL 令牌可以提供更多局部信息以改进重建，但因其不受 SSL 正则化约束，会破坏潜在空间结构，使生成质量迅速恶化。因此，极简的 1 令牌方案既是效率之源，也是多令牌扩展时的结构性障碍。
- **高精度重建场景的不适用性**：若目标应用对像素级保真度要求极高（如医学影像重建），当前的权衡曲线表明 PSNR 会停留在有限水平，需通过降低 λ 以换取重建质量，但这将严重损害生成能力。

以上结论均基于表中定量证据和附录中的定性对比，可复现性较强。对于文本到图像部分，由于仅提供零样本 FID 且未涵盖精细化空间控制实验，有关“物体定位与场景组合的细粒度控制”的限制尚需人工进一步核实。



## 定位与知识库关联

RepTok 的核心操作可以概括为一句话：**将一张图像压入一个连续向量，并在该向量上生成**。它在基线方法谱系中的位置与其他主流 tokenizer 存在根本差异，而这种差异正是其极简架构的前提。

### 从多维网格到单令牌的范式偏移

在 RepTok 之前，主流潜在扩散模型（LDM）依赖 VAE 编码器生成的 2D 网格潜在空间（通常 16×16），其本质是空间冗余的中间表征。TiTok 试图通过 32 个离散令牌压缩为 1D 序列，但依然保留了多令牌结构。FlexTok 进一步允许可变长度的连续令牌，却未跳出“多个令牌协作表示”的设定。RepTok 的突破在于：**证明单个连续 [cls] 令牌即可承载生成所需的全部信息**，将令牌数量从几十个骤降至 1，同时获得与 256 个令牌的 FlexTok 相当的生成质量（gFID 1.88 vs 1.86，Table 1）。这使 RepTok 既不依赖 2D 结构，也无需矢量量化或离散码本——它直接在 SSL 编码器天然形成的平滑连续空间中操作。与之形成对照，LDM 的 KL 正则化和 VQ‑VAE 的码本约束均是为了维持潜空间的可生成性，而 RepTok 通过余弦相似度损失即简单保留了这一性质。

### 自监督表征作为即插即用的生成空间

此前利用自监督表征加速扩散训练的方法（如 REPA）需要额外引入特征对齐损失，但本身并未改变扩散模型庞大的 Transformer 架构。RCG 虽将 SSL 特征作为条件却冻结整个编码器，导致重建细节严重丢失（rFID 3.20 vs RepTok 1.85，Table 3）。RepTok 的关键设计在于**仅微调 [cls] 令牌嵌入，而非整个编码器**。这种定点适配策略既能将重建所需的底层细节注入该令牌（Figure 5 显示冻结时细节大量丢失，微调后恢复），又避免了重训庞大编码器带来的计算开销。同时，附加的余弦相似度损失 $\mathcal{L}_{\mathrm{cos}} = \lambda(1 - \cos(z, z_{\mathrm{frozen}}))$ 强制微调后的向量维持与原 SSL 空间的方向一致性，从而保留了其平滑插值性质——Figure 4 证实语义和空间布局均能平滑过渡。这种“微调一点、正则化一点”的范式本质上是对 SSL 表征空间的最小侵入性改造，与以往联合训练整个编码器-解码器的做法截然不同。

### 轻量级生成器与训练效率的合力

RepTok 第二阶段生成器直接建模冻结编码器输出，这使其无需注意力机制即可用纯 MLP‑Mixer 架构完成生成（MLP‑Mixer 推理仅 0.27s，远小于解码器的 0.95s，Table 5）。相较之下，SiT/DiT 等 Transformer 基生成器在相同分辨率下需要数倍甚至数十倍的训练步数和计算量（Table 2 中 SiT‑XL/2 需 7M 步、FID 17.2，而 RepTok 仅 100K 步达到 5.4）。Figure 1 直观展示了 RepTok 训练 FLOPs 比 SiT‑B/2 减少 83%–92%。这一效率优势来源于两个因素的合力：**极低沉潜在维度（1×768）使得扩散/流匹配的运算成本大幅下降，以及生成模型本身可选用无注意力结构**。这是整个工作谱系中首次将预训练 SSL 空间直接用作生成模型输入，而非仅仅作为训练时的辅助信息。

### 适用边界与已知局限

尽管 RepTok 展现出了压倒性的效率优势，其有效性仍受若干条件制约。**该框架建立在强预训练视觉编码器（如 DINOv2）之上**，在编码器较弱或未进行良好自监督训练的场景下，极致的压缩会导致信息瓶颈灾难（Table 4 显示随机初始化编码器无法生成合理样本）。此外，余弦相似度正则化显式控制着重建与生成之间的权衡（Figure 9）：低 $\lambda$ 倾向高 PSNR 但导致极差 gFID，高 $\lambda$ 则相反。这种 trade‑off 使得**同时实现极高重建保真度与优异生成质量变得困难**，限制了该框架在对细节要求极严苛的重建任务中的适用性。

另一个边界在于单令牌表征的表达粒度。尽管一个 [cls] 令牌能捕捉全局语义和粗略空间布局，但其无法显式编码多个对象的精确位置关系。目前实现的插值平滑性主要作用于全局尺度，**细粒度控制对象位置与场景组合仍属开放问题**（part_005 分析明确指出）。此外，寄存器令牌虽然在重建 PSNR 上略优于 [cls] 令牌（12.85 vs 12.59，Table 6），但其空间未受 SSL 正则化约束，导致生成质量显著下降，这也再次印证了当前方法对 SSL 预训练结构的深度依赖。

最后，RepTok 的有效性验证目前集中于 ImageNet 256×256 和 MS‑COCO 零样本生成，其能否直接迁移至更高分辨率、视频生成或多模态理解等更复杂场景仍有待检验。论文 Supplementary 中提出的“如何扩展至更丰富的多令牌表示同时保持效率”这一问题，也折射出单令牌框架在信息容量上可能触及的天花板。



## 原文 PDF

PDF 文件：paperPDFs/ICLR_2026/Adapting_Self_Supervised_Representations_as_a_Latent_Space_for_Efficient_Generation.pdf

![[paperPDFs/ICLR_2026/Adapting_Self_Supervised_Representations_as_a_Latent_Space_for_Efficient_Generation.pdf]]

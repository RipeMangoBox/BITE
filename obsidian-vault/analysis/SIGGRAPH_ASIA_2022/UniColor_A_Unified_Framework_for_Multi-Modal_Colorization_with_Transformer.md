---
title: "UniColor: A Unified Framework for Multi-Modal Colorization with Transformer"
type: paper
paper_level: A
venue: SIGGRAPH ASIA
year: 2022
pdf_ref: paperPDFs/SIGGRAPH_ASIA_2022/UniColor_A_Unified_Framework_for_Multi_Modal_Colorization_with_Transformer.pdf
project_link: null
code_link: null
aliases:
- UniColor
tags:
- SIGGRAPH_ASIA_2022
- topic/vision_multimodal_applications
core_operator: 将多模态控制统一为提示点（hint points）的中间表示，并结合BERT式掩码训练，使单一Transformer模型可从任意位置的提示点完成色彩生成。
primary_logic: 通过将笔触、示例图像和文本描述统一转换为空间上的彩色提示点，并设计具有分离色度编码、混合连续/离散输入的Chroma-VQGAN和Hybrid-Transformer，首次实现多模态交互的多样化着色框架，在每一独立模态上均超越现有方法，并支持全新的混合控制。
claims:
- UniColor是首个支持混合多模态控制（笔触、示例、文本）的统一着色框架，用户研究偏好率达41%（无条件）、57%（笔触）、55%（示例）。
- UniColor在ImageNet无条件着色上实现FID 9.46、色彩丰富度39.01，优于CNN和纯Transformer基线。
- 所提出的Chroma-VQGAN和Hybrid-Transformer消融实验表明，保留连续灰度特征和连续提示点色彩显著降低FID（无条件9.46 vs 11.88；笔触7.04 vs 9.76）。
- CLIP驱动的文本到提示点转换无需训练即可定位开放词汇物体，使文本控制成为可能。
---

# UniColor: A Unified Framework for Multi-Modal Colorization with Transformer

> [!tip] 核心洞察
> 通过将笔触、示例图像和文本描述统一转换为空间上的彩色提示点，并设计具有分离色度编码、混合连续/离散输入的Chroma-VQGAN和Hybrid-Transformer，首次实现多模态交互的多样化着色框架，在每一独立模态上均超越现有方法，并支持全新的混合控制。

| 字段 | 内容 |
|------|------|
| 中文题名 | UniColor：面向多模态图像着色的统一Transformer框架 |
| 英文题名 | UniColor: A Unified Framework for Multi-Modal Colorization with Transformer |
| 会议/期刊 | SIGGRAPH ASIA 2022 |
| Links | [paper](https://luckyhzt.github.io/unicolor) |
| Topic | #topic/vision_multimodal_applications |
| Method | UniColor |
| Dataset | ImageNet, MSCOCO |

> [!tip] 效果简介
> - ImageNet (val, 256×256) 上，FID↓ / Colorfulness↑ 9.46 / 39.01 vs Coltran 22.17* (not directly comparable from Table 1, but overall best among ba... (显著更低FID，更高色彩丰富度)。
> - MSCOCO (val, 256×256) 上，FID↓ / Colorfulness↑ 11.16 / 39.11 vs Coltran trained on COCO (approx 24 FID, visual) [table excerpts] (大幅领先)。
> - ImageNet (unconditional variant, 256×256) 上，FID↓ 16.80 vs Coltran 19.37; Palette 15.78 (优于Coltran，与扩散模型Palette可比)。

## 概要

现有图像着色方法存在一个根本性瓶颈：不同控制模态（笔触、示例图像、文本描述）需要定制化的网络架构，无法在单一模型中统一处理混合多模态输入，而无条件方法则缺乏多样性与用户控制。UniColor 提出了首个统一的多模态着色框架，其核心思路是将笔触、示例和文本三种条件统一转换为空间上的“提示点”（hint points）这一中间表示，从而消除模态间的架构差异。在此基础上，方法设计了一个两阶段网络：Chroma-VQGAN 将图像分解为连续的灰度特征与量化的色度 token，保留结构细节；Hybrid-Transformer 以 BERT 式掩码训练接收混合格式输入（连续灰度特征、连续提示点颜色、量化色度 token），自回归生成多样化的着色结果。对于文本条件，利用 CLIP 零样本匹配将文本描述转换为提示点，无需额外训练。

实验表明，UniColor 在 ImageNet 无条件着色上达到 FID 9.46、色彩丰富度 39.01，优于 Coltran 等 Transformer 基线；在笔触、示例和文本三种独立模态上均超越对应专用方法，并在用户研究中获得 41%–57% 的偏好率。该方法首次实现了混合多模态交互着色，同时支持局部重着色和迭代编辑。

## 核心方法与创新机理

### 问题瓶颈与统一思路

现有多模态图像着色方法面临一个根本性瓶颈：笔触、示例图像和文本描述这三种主流控制模态各自需要定制化的网络架构，无法在单一模型中统一处理，更无法支持混合多模态输入。无条件着色方法虽能产生多样化结果，但缺乏用户控制能力。UniColor的核心洞察在于——这三种模态本质上都是在指定“哪些位置应该是什么颜色”，因此可以统一转化为一种共同的中间表示：**提示点（hint points）**，即一组带有目标颜色的空间点集合。

基于这一统一表示，UniColor设计了一个两阶段框架（Fig. 2）：
- **第一阶段（Hint Points Conversion）**：将笔触、示例图像和文本描述分别转换为统一的彩色提示点集合；
- **第二阶段（Diverse Unified Colorization）**：以灰度图像和提示点为条件，通过Chroma-VQGAN与Hybrid-Transformer的组合网络，生成多样化的着色结果。

![[assets/figures/papers/paper_list_l97_https_luckyhzt_github_io_unicolor/figures/002_Figure_2.jpg]]
*Figure 2: Our unified colorization pipeline. The pipeline consists of two stages. In the first stage, all different conditions are unified as hint points. In the second stage, diverse results are generated automatically either from scratch or based on the condition of hint points. Input images: the 1???? row is from ImageNet and all others are from MSCOCO*

整个框架的数学目标可表述为从条件概率分布中采样多样化的彩色图像：

$$\{ \hat { I } _ { c } ^ { i } \} \sim P ( \hat { I } _ { c } | I _ { g } , \mathbb { H } ( \mathbb { P } ( \{ s , I _ { r } , t \} ) ) )$$

其中 $I_g$ 为输入灰度图像，$\mathbb{P}$ 为多模态条件（笔触 $s$、示例 $I_r$、文本 $t$），$\mathbb{H}$ 为提示点转换函数，$\hat{I}_c^i$ 为第 $i$ 个多样化的彩色输出。

### Changed Slot 1：条件表示——从模态特定到统一提示点

**基线值**：各模态采用独立的条件表示和注入方式（笔触直接作为颜色约束图、示例通过特征匹配传递、文本通过语言编码器映射）。

**提出值**：所有模态统一转化为空间上的彩色提示点集合 $\mathbb{H}$，即 $\{(\text{位置}, \text{RGB颜色})\}$ 的集合。

三种模态的转换机制（Fig. 3）：
- **笔触→提示点**：沿用户绘制的笔触轨迹遍历网格单元，若单元内着色像素比例超过阈值（如0.75），则将该单元标记为提示点，并取笔触颜色的均值作为目标颜色。
- **示例→提示点**：将示例图像与灰度输入进行密集特征匹配（使用预训练的VGG特征），为每个空间位置找到示例中最相似的特征位置，并将对应颜色作为提示点颜色。为减少噪声，仅在匹配置信度高的位置保留提示点。
- **文本→提示点**：提出一种基于CLIP的零样本转换方法。将图像划分为网格单元，对每个文本描述中的物体概念，计算各单元与文本的CLIP嵌入相似度，得到对应关系图（correspondence map），选取top-2相似度单元作为该概念的提示点，并从预定义颜色表中分配颜色。

这一设计的关键因果效应在于：提示点表示将异构的条件信息统一为空间-颜色的结构化形式，使得下游网络只需处理单一类型的条件输入，无需为每种模态设计独立的编码器和融合模块。

### Changed Slot 2：VQGAN设计——从全图量化到分离色度编码（Chroma-VQGAN）

**基线值**：标准VQGAN将整张RGB图像编码为统一的离散码本表示，灰度结构信息也被量化，导致结构细节丢失。

**提出值**：Chroma-VQGAN采用双分支编码器设计（Fig. 4a），将色度信息与灰度结构信息分离处理：
- **灰度编码器**：提取连续灰度特征 $f_g$，**保持不量化**，以保留精确的结构和纹理细节；
- **色度编码器**：提取色度特征 $f_c$，通过码本 $\mathcal{Z} = \{z_k\}_{k=0}^{N-1}$ 进行向量量化，得到离散色度token序列 $x_c$。

色度特征的标记化过程为最近邻查找：

$$x _ { c } ^ { i j } = \underset { k \in [ 0 , N - 1 ] } { \arg \min } ~ \| f _ { c } ^ { i j } - z _ { k } \|$$

解码时，将量化的色度特征 $\hat{f}_c$ 与连续灰度特征 $f_g$ 拼接后输入联合解码器，重建彩色图像。

这一分离设计的因果机制：灰度特征保持连续避免了量化带来的信息损失，使重建图像保留清晰的边缘和纹理；色度特征的离散化则为后续Transformer的离散token预测提供了基础，同时码本学习本身也起到了色度空间的规整化作用。

### Changed Slot 3：色彩预测主干——从纯离散Transformer到混合Transformer（Hybrid-Transformer）

**基线值**：Coltran等纯Transformer方法将所有信息（包括灰度）都量化为离散token，通过自回归方式逐token预测颜色。

**提出值**：Hybrid-Transformer同时接收三种不同格式的输入（Fig. 4b）：
- **离散色度token** $x_c^{\bar{M}}$（未被掩蔽的部分）：通过可学习的token嵌入投影到Transformer维度；
- **连续灰度特征** $f_g$：通过线性层直接投影，保留连续值精度；
- **连续提示点颜色** $h_c$：通过可学习权重 $W_h$ 和位置嵌入 $p_h$ 映射到特征空间：

$$f_h = W_h h_c + p_h$$

其中 $W_h \in \mathbb{R}^{3 \times d_e}$，$d_e$ 为Transformer的嵌入维度。

**训练路径（BERT式掩码色彩补全）**：与自回归逐token预测不同，UniColor采用BERT式训练策略。训练时随机掩蔽部分色度token（掩蔽比例约15-50%），模型以未掩蔽的色度token $x_c^{\bar{M}}$、连续灰度特征 $f_g$ 和提示点特征 $f_h$ 为条件，预测掩蔽位置的色度索引。条件似然函数为：

$$P(x_c^M | x_c^{\bar{M}}, f_g, f_h) = \prod_{i \in M} P(x_c^i | x_c^{\bar{M}}, f_g, f_h)$$

**推理路径（自回归采样）**：推理时采用光栅扫描顺序的自回归采样策略。初始时所有色度token均被掩蔽（无条件模式）或部分位置由提示点指定（有条件模式），模型按从左到右、从上到下的顺序逐个预测每个位置的色度token：

$$\hat{p}(\hat{x}_c | f_g, f_h) = \prod_i \hat{p}(\hat{x}_c^i | \hat{x}_c^{<i}, f_g, f_h)$$

每次采样时，从预测的概率分布中按温度参数采样一个色度索引，将其填入对应位置后作为后续预测的条件。通过调整采样温度或进行多次独立采样，即可获得多样化的着色结果。

**模块间因果关系**：Chroma-VQGAN提供的连续灰度特征 $f_g$ 为Hybrid-Transformer保留了精确的结构信息，使Transformer能够专注于色度预测而非结构重建；提示点特征 $f_h$ 通过位置嵌入与对应空间位置的色度token建立直接关联，使条件信息能够精确地约束局部颜色预测；BERT式训练使模型学会从部分色度信息推断全局色彩分布，这是实现多样化的关键——不同的随机掩蔽模式和采样顺序自然产生不同的色彩方案。

### 交互界面与混合控制

UniColor还提供了一个交互式界面（Fig. 5），支持用户通过笔触绘制、示例图像上传和文本输入三种方式施加着色控制。该界面的核心价值在于支持**混合模态控制**：用户可同时对不同区域使用不同模态的条件（如用笔触指定前景物体颜色、用文本描述背景场景），所有条件被统一转换为提示点后输入同一网络，实现无缝的混合控制着色。此外，框架还支持局部重着色（选定区域后施加新条件重新生成）和迭代编辑（对老照片进行多轮颜色调整），这些能力均源于提示点表示的空间局部性和Hybrid-Transformer的条件采样灵活性。

### 关键公式变量含义汇总

| 符号 | 含义 |
|------|------|
| $I_g$ | 输入灰度图像 |
| $I_c$ / $\hat{I}_c$ | 真实/生成的彩色图像 |
| $\mathbb{H}$ | 提示点集合（位置+RGB颜色） |
| $f_g$ | 连续灰度特征（Chroma-VQGAN灰度编码器输出） |
| $f_c$ | 色度特征（Chroma-VQGAN色度编码器输出） |
| $x_c$ | 量化的色度token索引序列 |
| $\mathcal{Z} = \{z_k\}$ | VQGAN可学习码本，$N$为码本大小 |
| $x_c^M$ / $x_c^{\bar{M}}$ | 被掩蔽/未被掩蔽的色度token集合 |
| $f_h$ | 提示点映射后的特征向量 |
| $W_h, p_h$ | 提示点线性投影权重和位置嵌入 |

![[assets/figures/papers/paper_list_l97_https_luckyhzt_github_io_unicolor/figures/001_Figure_1.jpg]]
*Figure 1: Given an input grayscale image, our unified framework UniColor is able to: (a) produce diverse colorization results unconditionally*

![[assets/figures/papers/paper_list_l97_https_luckyhzt_github_io_unicolor/figures/004_Figure_4.jpg]]
*Figure 4: Architecture of diverse unified colorization network. The network consists of two sub-nets: (a) a Chroma-VQGAN to disentangle and quantize chroma representation from the continuous gray one, and (b) a Hybrid-Transformer to generate diverse colorization results from unified conditions and continuous gray features. Input image: from ImageNet*

## 实验与关键发现

### 无条件着色主结果

UniColor在ImageNet和MSCOCO两个标准基准上均取得领先的无条件着色性能（Table 1）。在ImageNet验证集（256×256）上，UniColor的FID达到**9.46**，色彩丰富度（Colorfulness）为**39.01**，显著优于CNN方法InstColor（FID 10.31）和ChromaGAN（FID 24.56），也明显超越纯Transformer基线Coltran（FID 22.17，但需注意此Coltran结果来自原论文、训练设置不完全对齐）。在MSCOCO验证集上，UniColor的FID为**11.16**，色彩丰富度**39.11**，同样大幅领先Coltran在COCO上训练的版本（FID约24）。与扩散模型Palette（FID 15.78）相比，UniColor的FID更低（9.46 vs 15.78），表明基于VQGAN+Hybrid-Transformer的离散-连续混合方案在无条件着色质量上可与扩散模型竞争甚至超越。

![[assets/figures/papers/paper_list_l97_https_luckyhzt_github_io_unicolor/figures/006_Table_1.jpg]]
*Table 1: Comparison with unconditional colorization methods on both ImageNet and MSCOCO datasets. The models are trained on ImageNet if not specified (* Trained on MSCOCO). Metrics calculated on original images are taken as references*

定性对比（Fig. 6、Fig. 7）显示，UniColor生成的结果在色彩鲜艳度和自然度上均优于InstColor和ChromaGAN，且能产生与Palette相当的多样化结果。

![[assets/figures/papers/paper_list_l97_https_luckyhzt_github_io_unicolor/figures/007_Figure_6.jpg]]
*Figure 6: Comparison with unconditional colorization methods: InstColor [Su et al. 2020], ChromaGAN [Vitoria et al. 2020], and Coltran [Kumar et al. 2021]. Our model can generate diverse results for each of the input grayscale images. Input images: the*

![[assets/figures/papers/paper_list_l97_https_luckyhzt_github_io_unicolor/figures/008_Figure_7.jpg]]
*Figure 7: Comparison with diffusion-based model Palette [Saharia et al. 2021]. Our method generates diverse results comparable to Palette. Input images: from ImageNet*

### 条件着色性能

**笔触着色**（Table 2）：在ImageNet上引入笔触条件后，UniColor的FID从无条件变体的9.46大幅降至**7.04**，验证了提示点条件对色彩预测的有效引导。与User-guided方法（Zhang et al., TOG 2017）相比，UniColor在相同笔触输入下生成的结果色彩更自然、与灰度结构更一致（Fig. 8）。

**示例着色**（Table 3）：在ImageNet上，UniColor的FID为**7.39**，优于Deep Exemplar-based方法（He et al., TOG 2018）的8.21。UniColor通过将示例图像的颜色统计转化为空间提示点，避免了传统示例方法中复杂的颜色匹配和传递过程，同时保持了色彩迁移的准确性（Fig. 9）。

**文本着色**（Table 4）：在MSCOCO上，以CLIP相似度衡量文本-图像一致性，文本条件变体达到**24.50**，相比无条件变体的21.48提升了**+3.02**，证明CLIP驱动的文本到提示点转换能有效将开放词汇物体描述映射为空间颜色引导。与Learn-Color-Lang（Manjunatha et al., NAACL 2018）相比，UniColor在相同文本输入下生成的颜色更符合语义预期（Fig. 10）。

### 用户研究

三组用户研究（Fig. 11）覆盖无条件、笔触和示例着色任务，每项任务邀请参与者从UniColor与对应基线方法中选出更偏好的结果。结果显示：无条件任务中UniColor偏好率为**41%**，笔触任务为**57%**，示例任务为**55%**——在所有任务中均被更频繁地选择为更优结果。这验证了统一框架不仅在定量指标上领先，在人类主观感知层面也具备优势。

### 关键消融实验

**Chroma-VQGAN的有效性**（Table 5）：在图像重建任务上，Chroma-VQGAN（保留连续灰度特征）的FID为**1.68**，显著优于标准VQGAN的2.84和量化灰度变体Quant-VQGAN的2.42。这表明分离色度与灰度编码、保持灰度特征连续的设计，有效保留了结构细节，避免了因灰度量化导致的模糊和伪影（Fig. 12）。

**Hybrid-Transformer中连续特征的作用**（Table 6）：将连续灰度特征替换为离散token（Quant-gray）后，无条件着色FID从9.46恶化至**11.88**（+2.42）；将连续提示点颜色替换为离散token（Quant-hint）后，笔触着色FID从7.04恶化至**9.76**（+2.72）。这两项消融直接证明了混合连续-离散输入设计是UniColor性能的关键——连续灰度特征保留了结构信息，连续提示点颜色保留了精确的色彩引导，二者共同使Transformer能更准确地完成色彩补全。

### 失败模式与适用边界

**语义不合理颜色**（Fig. 18）：由于推理时采用自回归随机采样，模型可能在某些位置生成语义不合理的颜色，例如绿色道路、棕色西兰花。这是因为采样过程缺乏对颜色语义合理性的显式约束，仅依赖训练数据中的统计规律。

**多模态控制冲突**：当不同模态的提示点在同一区域指定冲突颜色时（如文本提示点要求“红色”而笔触指定绿色），模型可能产生不可预见的中间色或混合色（Fig. 18）。框架目前未引入冲突检测或优先级机制。

**文本定位精度有限**：文本到提示点的转换依赖CLIP零样本匹配，对复杂文本描述（如“穿蓝色条纹衬衫的人”）的物体定位可能不准确，且依赖固定的颜色表，不支持细粒度的颜色描述（如“深海军蓝”）。该模块的优势在于无需训练即可处理开放词汇，但精度受限于CLIP本身的定位能力。

**适用边界**：UniColor的训练数据为ImageNet和MSCOCO，对特定领域（如医学图像、遥感图像）或训练集中覆盖不足的类别可能存在色彩偏差。框架目前整合了笔触、示例和文本三种模态，尚未扩展到调色板、语义布局等其他交互形式。

## 定位与知识库关联

UniColor 的核心定位是 **将图像着色问题从单模态条件控制推进到统一多模态框架**，其本质改变在于 **条件表示槽位（condition representation slot）** 的重新设计。在现有工作中，笔触着色（如 **User-guided** Zhang et al., TOG 2017）、示例着色（如 **Deep Exemplar-based** He et al., TOG 2018）和文本着色（如 **Learn-Color-Lang** Manjunatha et al., NAACL 2018）各自采用定制化的条件编码方式——笔触通过局部仿射传播、示例通过全局风格匹配、文本通过语言编码器映射，三者架构互不兼容。UniColor 将这一槽位从“模态特定编码器”替换为“统一空间提示点（hint points）中间表示”，使得单一 Transformer 骨干可同时接收来自笔触、示例图像和文本描述的条件信号，首次实现混合多模态交互式着色。

与无条件着色基线相比，UniColor 在 **色彩预测主干网络槽位** 上同样做出了关键改动。**Coltran**（Kumar et al., ICLR 2021）采用纯 Transformer 对完全量化的离散 token 进行自回归预测，其灰度信息也被离散化，导致结构细节丢失；**Palette**（Saharia et al., arXiv 2021）则依赖扩散模型的迭代去噪。UniColor 提出的 **Hybrid-Transformer** 同时接收连续灰度特征、连续提示点颜色和量化的色度 token，通过 BERT 式掩码补全训练实现单步多样化生成，在 FID 指标上显著优于 Coltran（ImageNet 无条件 9.46 vs 19.37），并与扩散模型 Palette（15.78）可比甚至更优。

在 **VQGAN 设计槽位** 上，标准 VQGAN 将整张图像（包括灰度结构信息）统一编码为离散码本，重建时容易丢失高频细节。UniColor 的 **Chroma-VQGAN** 采用分离的色度编码器与灰度编码器，仅对色度特征进行量化而保留连续灰度特征，这一改动在图像重建消融中使 FID 从标准 VQGAN 的 2.84 降至 1.68（Table 5），为下游着色任务提供了更可靠的结构基础。

### 知识库挂载点

UniColor 可挂载到以下知识库节点：

1. **多模态条件融合（Multimodal Condition Fusion）**：作为将异构控制信号统一为空间提示点的典型案例，与 ControlNet 系列（通过空间条件图统一控制）形成方法论对照，但 UniColor 更强调跨模态的零样本转换（如 CLIP 驱动的文本到提示点映射）。

2. **BERT 式生成式视觉模型**：UniColor 将 BERT 掩码预训练范式从自然语言处理迁移到色彩生成任务，与 MAGE（Li et al., CVPR 2023）等掩码图像建模方法共享“从部分观测重建完整信号”的核心思想，但 UniColor 的掩码对象是色度 token 而非原始像素，且条件信号（灰度特征、提示点）始终保持完整。

3. **VQGAN 架构变体**：Chroma-VQGAN 的分离编码设计可归入“解耦表示学习 + 矢量量化”技术线，与将语义与纹理分离的 VQGAN 变体（如 StyleGAN-VQ）形成互补，为需要保留连续结构信息的图像翻译任务提供参考架构。

4. **交互式图像编辑工具链**：UniColor 提供的笔触、示例、文本混合控制界面以及局部重着色、迭代编辑功能，可挂载到交互式图像编辑系统知识库，与 Photoshop Neural Filters、DragGAN 等工具在用户控制灵活性和生成多样性维度上进行比较。

### 适用边界与局限

UniColor 的统一框架在以下边界内有效：

- **模态覆盖范围**：当前仅整合笔触、示例和文本三种模态，尚未扩展到调色板、语义布局、属性标签等其他潜在控制形式。框架的提示点表示理论上可容纳更多模态，但需为每种新模态设计专门的转换策略。
- **文本控制精度**：文本到提示点的转换依赖 CLIP 零样本匹配，对复杂文本描述（如“深红色的玫瑰花蕾”）的物体定位精度有限，且依赖预定义的固定颜色表，不支持细粒度颜色描述的直接映射。
- **随机采样风险**：BERT 式掩码补全训练虽能生成多样化结果，但随机采样过程缺乏对语义合理性的约束，可能出现绿色道路、棕色西兰花等意外着色（Fig. 18）。这一局限源于训练目标仅优化色度 token 的似然，未引入语义一致性正则。
- **控制冲突处理**：当不同模态在同一区域指定冲突颜色时（如笔触指定红色、文本提示点指定绿色），模型可能产生不可预见的中间色，框架未内置冲突检测或仲裁机制。
- **数据分布偏差**：训练仅使用 ImageNet 和 MSCOCO，对特定类别或场景（如医学图像、遥感影像）的泛化能力未经验证。

### 后续启发与开放方向

UniColor 的统一提示点范式为以下方向提供了直接启发：

1. **采样质量控制**：如何在保持多样性的同时限制随机采样范围以避免意外颜色？可引入语义质量网络对生成结果进行自动筛选，或在采样过程中加入基于 CLIP 语义相似度的约束项。

2. **控制冲突自动解决**：能否基于图像分割自动检测来自不同模态的提示点冲突区域，并通过优先级策略（如笔触优先级高于文本）或颜色混合模型进行仲裁？

3. **模态扩展**：该统一提示点表示能否扩展到视频着色（将时序光流作为额外条件）、调色板驱动着色（将调色板颜色分配到语义区域）、或草图引导着色等任务？

4. **训练策略改进**：当前 BERT 式训练在无条件生成时需自回归逐 token 采样，推理速度受限于序列长度。是否可引入非自回归解码策略（如并行迭代解码）以加速推理，同时维持生成质量？

5. **与其他生成范式的融合**：Hybrid-Transformer 的连续-离散混合输入设计能否与扩散模型结合，在去噪过程中注入连续灰度特征以提升结构保真度？这将是连接 Transformer 与扩散模型两条技术线的一个有价值切入点。

## 原文 PDF

![[paperPDFs/SIGGRAPH_ASIA_2022/UniColor_A_Unified_Framework_for_Multi_Modal_Colorization_with_Transformer.pdf]]
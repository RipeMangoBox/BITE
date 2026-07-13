---
title: "Retrieve-to-Restore: Efficient All-in-One Image Restoration with a Retrieval-Based Degradation Bank"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Retrieve_to_Restore_Efficient_All_in_One_Image_Restoration_with_a_Retrieval_Based_Degradation_Bank.pdf
project_link: null
code_link: "https://github.com/cscxwang/R2R"
aliases:
- RRR
- Retrieve-to-Restore
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 将退化知识与主干解耦，用外部检索式的退化知识库取代内部调制（提示、MoE路由等），显式分离退化线索与共享重建能力。
primary_logic: 退化类型表现出明显的类内相似性和类间可分性（如雨纹、雾、噪声的独特结构），可用紧凑的统一任务级先验表示；在推理时按需检索相关先验来调节卷积特征，从而在轻量级共享主干上实现稳定、高效的多退化恢复。
claims:
- R2R在三个退化任务上的平均PSNR达到32.53 dB，而计算量仅为12G MACs，比PromptIR减少约91%。
- 随着退化类型从1种增加到3种再到5种，R2R的性能下降幅度显著小于Gridformer、PromptIR等方法，即任务鲁棒性最优。
- 消融实验表明，在L1重建损失基础上引入退化分类损失、匹配损失和频域损失可带来0.65dB的平均PSNR增益。
- 退化银行可由低质量图像构建，仅比使用干净图像构建损失0.2dB，证明该方法对HQ数据的依赖性较低。
---

# Retrieve-to-Restore: Efficient All-in-One Image Restoration with a Retrieval-Based Degradation Bank

> [!tip] 核心洞察
> 退化类型表现出明显的类内相似性和类间可分性（如雨纹、雾、噪声的独特结构），可用紧凑的统一任务级先验表示；在推理时按需检索相关先验来调节卷积特征，从而在轻量级共享主干上实现稳定、高效的多退化恢复。

| 字段 | 内容 |
|------|------|
| 中文题名 | 检索即恢复：基于检索式退化知识库的高效一体化图像恢复 |
| 英文题名 | Retrieve-to-Restore: Efficient All-in-One Image Restoration with a Retrieval-Based Degradation Bank |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Wang_Retrieve-to-Restore_Efficient_All-in-One_Image_Restoration_with_a_Retrieval-Based_Degradation_Bank_CVPR_2026_paper.html) · [Code](https://github.com/cscxwang/R2R) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | Retrieve-to-Restore (R2R) |
| Dataset | Three degradations, Five degradations, Single degradation dehazing, Single degradation deraining |

> [!tip] 效果简介
> - Three degradations (SOTS, Rain100L, BSD68 σ=15/25/50) 上，Average PSNR / SSIM 32.53 / 0.918 vs PromptIR: 32.06 / 0.913 (+0.47 dB / +0.005)。
> - Five degradations (SOTS, Rain100L, BSD68, GoPro, LOL) 上，Average PSNR / SSIM 30.48 / 0.921 vs AirNet: 26.04 / 0.874 (estimated) (+4.44 dB / +0.047)。
> - Single degradation dehazing (SOTS) 上，PSNR / SSIM 31.50 / 0.978 vs Gridformer: 30.37 / 0.970 (+1.13 dB / +0.008)。

## 概要

### 问题背景

图像恢复任务（去雾、去雨、去噪、去模糊、低光增强等）传统上依赖任务专用模型，但真实场景中退化类型往往未知且多样，催生了“一体化”（all-in-one）恢复方法的需求。这类方法旨在用单一模型处理多种退化，其核心瓶颈在于：**联合训练多种退化时，共享主干网络中存在参数专业化冲突，导致任务间干扰和优化不稳定，严重制约了性能上限**。现有方案试图通过内部提示（如 **PromptIR**, Potlapalli et al., NeurIPS 2023）、MoE路由或对比学习（如 **AirNet**, Li et al., CVPR 2022）来缓解此问题，但这些机制仍嵌入主干内部，未能从根本上解耦退化知识与共享重建能力。

### 核心思想

本文提出 **Retrieve-to-Restore (R2R)**，其核心洞察是：**退化类型表现出明显的类内相似性和类间可分性**（如雨纹、雾、噪声各自具有独特的结构模式），因此可用紧凑的统一任务级先验表示。R2R将退化知识从主干中彻底外置，构建一个**检索式退化知识库（Degradation Bank）**，在推理时按需检索相关先验来调节卷积特征，从而让轻量级共享主干仅承担任务无关的重建工作。这一设计直接切断了参数冲突的根源。

### 方法定位

R2R的方法学谱系位于“外部知识引导的一体化恢复”这一新兴方向，与基于提示、MoE或对比学习的内部调制方案形成鲜明分野。其关键差异在于：

| 设计维度 | 基线方案（内部调制） | R2R（外部检索） |
|---------|---------------------|-----------------|
| 退化适应机制 | 视觉/文本提示或MoE路由，嵌入主干内部 | 外部退化知识库，通过匹配模块在主干最低层注入先验 |
| 计算效率 | PromptIR需132G MACs，Gridformer需251G MACs | **12G MACs**（约减少91%） |
| 训练稳定性 | 多退化联合训练时参数更新方向冲突 | 退化信息外置，主干参数更新一致性好 |
| 先验构建方式 | 通常需要干净目标图像 | 可用干净或退化的低质量图像构建，仅轻微性能损失 |

在知识库定位上，R2R可视为将“检索增强生成”（RAG）范式引入图像恢复领域的尝试——退化银行类比于外部知识库，退化匹配模块类比于检索器，共享主干类比于生成器。该方法与 **NAFNet** (Chen et al., NeurIPS 2022) 共享基础架构，但通过外部先验注入实现了从任务专用到一体化的跨越。

### 主要结果

R2R在效率与性能的权衡上取得了显著突破。如 Figure 1 所示，**R2R在三个退化任务上的平均PSNR达到32.53 dB，而计算量仅为12G MACs，比PromptIR减少约91%，同时PSNR提升0.47 dB**。在五退化设置下（Table 2），R2R的平均PSNR达到30.48 dB，较AirNet提升约4.44 dB。即使在单退化任务上（Table 3），R2R也表现出竞争力：去雾（SOTS）31.50 dB，去雨（Rain100L）37.45 dB，超过 **Gridformer** (Wang et al., IJCV 2024) 和 **Restormer** 等专用方法。

任务鲁棒性实验（Figure 3）进一步验证了设计的有效性：**随着退化类型从1种增加到3种再到5种，R2R的性能下降幅度显著小于Gridformer、PromptIR等方法**，体现了外部解耦策略在抑制任务间干扰方面的优势。消融实验（Table 6）表明，在L1重建损失基础上引入退化分类损失、匹配损失和频域损失可带来**0.65 dB的平均PSNR增益**，验证了多损失联合优化的必要性。此外，退化银行可由低质量图像构建，仅比使用干净图像构建损失0.2 dB（Table 7），证明该方法对高质量数据的依赖性较低。

### 局限与展望

R2R的主要局限在于：退化银行的构建需要预定义退化类型，无法直接处理完全未知的新退化类别；目前仅支持离散的退化类型，对混合退化或连续退化强度的直接支持尚不明确。未来方向包括将检索式先验扩展到视频恢复、利用视觉-语言模型提供更高层次的语义先验以增强泛化能力，以及探索检索到的先验在生成式恢复（如扩散模型）中的应用。



图像恢复旨在从退化的低质量观测中重建高质量图像，是计算机视觉领域的基础问题。真实场景中的退化类型多样，包括雾霾、雨纹、噪声、模糊和低光照等。传统方法通常为每种退化单独训练一个专用模型，这不仅增加了部署成本，也忽略了不同退化任务之间的潜在共享知识。近年来，一体化图像恢复（All-in-One Image Restoration）范式应运而生，试图用单一模型处理多种退化类型。

### 核心瓶颈：参数专业化冲突

当前一体化方法面临的根本瓶颈在于**参数专业化冲突**。当多种退化类型在共享主干网络中联合训练时，不同任务的梯度更新方向可能相互矛盾——例如，去雾任务需要增强边缘对比度，而去噪任务倾向于平滑纹理。这种冲突导致优化不稳定，严重制约了一体化模型的性能上限。现有方法试图通过内部调制机制来缓解这一问题：**PromptIR**（Potlapalli et al., NeurIPS 2023）采用视觉提示嵌入主干内部来区分退化类型，**AirNet**（Li et al., CVPR 2022）利用对比学习提取退化感知特征，**Gridformer**（Wang et al., IJCV 2024）则通过Transformer架构隐式建模退化差异。然而，这些方法仍将退化知识与共享重建能力耦合在同一参数空间中，未能从根本上解决冲突。

### 因果机制：退化知识的解耦

本文的核心洞察在于：**退化类型表现出明显的类内相似性和类间可分性**。雨纹的条纹结构、雾霾的全局散射效应、噪声的随机分布模式，各自具有独特的视觉特征，可以被紧凑的统一任务级先验所表征。这一观察暗示了一个关键的因果调节变量——将退化知识与主干网络解耦，用外部检索式的退化知识库取代内部调制。具体而言，退化线索应当显式地从共享重建能力中分离出来：主干网络仅承担任务无关的特征提取与重建，而退化特定的先验信息按需从外部知识库中检索并注入。

### 现有方法的效率困境

除参数冲突外，计算效率也是一体化方法面临的重要挑战。以PromptIR为例，其计算量高达132G MACs，Gridformer更达到251G MACs，这严重限制了在资源受限设备上的部署。高计算开销的根源在于，内部调制机制通常需要额外的网络分支或注意力操作来处理退化信息，而这些操作与主干网络的计算深度耦合，无法独立优化。

### 本文动机与目标

基于上述分析，本文提出**Retrieve-to-Restore（R2R）**框架，遵循“编码-检索-解码”（Encode-Retrieve-Decode）范式。核心设计原则是将退化知识外置为紧凑的退化银行（Degradation Bank），在推理时按需检索相关先验来调节卷积特征，从而在轻量级共享主干上实现稳定、高效的多退化恢复。该方法旨在同时解决参数专业化冲突和计算效率两大瓶颈，为一体化图像恢复提供新的技术路径。



## 核心方法与创新机理

R2R的核心创新在于将退化适应机制从主干网络内部彻底剥离，引入外部检索式退化知识库，从根本上解决了多退化联合训练中的参数冲突瓶颈。具体而言，该方法在以下四个关键维度上实现了对现有范式的突破。

### 从内部调制到外部解耦：退化知识库的构建与检索

现有的一体化恢复方法普遍将退化信息嵌入主干内部——**PromptIR**（Potlapalli et al., NeurIPS 2023）依赖视觉提示向量调节特征，**AirNet**（Li et al., CVPR 2022）通过对比学习编码退化类型，而基于MoE路由的方法则在网络中动态选择专家分支。这些内部调制策略使得共享参数在优化时被迫同时适应多种退化的冲突更新方向，导致训练不稳定且性能上限受限。

R2R将退化知识外化为紧凑的**退化知识银行**（Degradation Bank），通过“编码-检索-解码”范式实现退化线索与共享重建能力的显式分离。训练阶段，**退化融合器**（Degradation Amalgamator）利用成对数据为每种退化学习统一的任务级先验，将其存储为键-值对；推理阶段，**退化匹配模块**（Degradation Matching Module）通过全局相似度矩阵 $S = D_K \times U_K^T$ 计算查询特征与银行键的匹配度，经局部平均与掩码操作后检索出最相关的干净先验，再通过门控卷积与查询特征融合，生成锐化先验以指导解码。这一设计使主干网络仅承担任务无关的共享重建，参数更新方向一致，训练稳定性显著提升。

### 极致的效率-性能权衡

R2R在计算效率上实现了数量级突破。基于NAFNet的轻量级U形编码器-解码器主干，配合外部检索机制，R2R在224×224输入下的计算量仅为**12G MACs**，参数量**19.7M**，推理内存**846MB**。相比之下，PromptIR需132G MACs，Gridformer（Wang et al., IJCV 2024）需251G MACs——R2R在取得更高平均PSNR的同时，计算量减少了约**91%**。这一效率优势源于退化信息的按需检索而非持续计算：银行中的先验仅在最低层特征处注入一次，无需在每个模块中重复编码退化条件。

### 任务鲁棒性的结构性提升

随着退化类型从1种增至3种再增至5种，R2R的PSNR降幅控制在**0.5dB以内**，远小于Gridformer、PromptIR等方法的显著下降。这一任务鲁棒性来源于架构层面的结构性优势：新增退化类型仅需在银行中增加相应的任务级先验，主干网络的共享重建能力不受干扰，避免了内部调制方法中参数空间随任务数量膨胀而加剧冲突的问题。

### 对高质量数据依赖的降低

传统先验构建方法通常需要干净目标图像作为参考。R2R的退化银行可由低质量图像构建，仅比使用干净HQ图像构建损失**0.2dB**平均PSNR（32.33 vs 32.53）。这一特性降低了方法对高质量配对数据的依赖，拓宽了实际部署场景的适用性。

**证据强度说明**：上述核心创新的关键主张均有高置信度实验证据支撑。效率-性能权衡由Table 1、Table 4和Figure 1联合验证（置信度0.95）；任务鲁棒性由Figure 3支撑（置信度0.9）；HQ数据依赖性由Table 7验证（置信度0.95）。



R2R 的整体架构遵循“编码—检索—解码”范式，将退化先验与共享重建能力彻底解耦。系统由三个核心模块构成：基于 NAFBlock 的 U 型编码器-解码器、退化融合器，以及退化匹配模块。

**信息流概览。** 给定一幅退化图像，编码器首先提取多尺度特征图。在编码器的最底层，退化匹配模块以编码特征作为查询，从预构建的退化知识银行中检索出与当前退化类型最匹配的任务级干净先验。该先验通过门控卷积与查询特征融合后，注入解码器的跳跃连接，逐级引导重建过程。最终，解码器输出恢复后的干净图像。

**编码器-解码器主干。** 主干采用对称的四层 U 型结构，基于 **NAFNet**（Chen et al., NeurIPS 2022）的 NAFBlock 构建。编码器各层 NAFBlock 数量自上而下为 [1, 1, 1, 28]，解码器与之对称。该主干不包含任何退化特定的调制参数，仅承担任务无关的共享特征提取与重建，从而避免了多退化联合训练时的参数冲突。

**退化知识银行。** 退化银行存储了每种退化类型对应的统一任务级先验，由退化融合器在训练阶段离线构建。银行以键-值对的形式组织：键用于退化匹配，值则提供恢复所需的干净特征先验。银行容量由超参数 M 控制，实验表明 M=64 时达到最佳性能-效率平衡。

**退化匹配与先验注入。** 推理时，退化匹配模块计算查询特征与银行所有键的全局相似度矩阵，经局部均值池化和掩码操作锁定最匹配的退化类型，再通过 Softmax 加权聚合对应的值特征。聚合后的先验与查询特征沿通道维度交叉级联，送入门控卷积模块生成锐化先验，最终注入解码器以指导恢复。门控卷积采用分组数为 C_v 的 3×3 分组卷积，确保每个退化样本仅与其检索到的先验交互。

**端到端训练。** R2R 框架完全端到端可训练，无需任何组件的多阶段优化。训练损失由像素域 L1、频域 L1、退化分类损失和匹配损失联合组成，权重分别为 1.0、0.125、0.1、0.1。

### 补充图表

![[assets/figures/papers/paper_list_l925_https_openaccess_thecvf_com_content_CVPR2026_html_Wang_Retrieve_to_Resto/figures/002_Figure_2.jpg]]
*Figure 2: (a) Overall framework of the proposed R2R. R2R mainly consists of NAFBlocks [4] based U-shaped encoder–decoder, a degradation amalgamator, and a degradation matching module. (b) The degradation amalgamator identifies degradation types and encodes the corresponding clean images into a unified prior space to construct the degradation bank. (c) The degradation matching module enables the degraded input to query the bank and retrieve relevant clean priors to guide restoration*



R2R（Retrieve-to-Restore）的整体架构遵循“编码-检索-解码”范式，由三个核心组件构成：**基于NAFBlock的U型编码器-解码器**、**退化融合器（Degradation Amalgamator）**和**退化匹配模块（Degradation Matching Module）**，如Figure 2所示。

### 退化融合器与退化知识银行

退化融合器在训练阶段负责将成对数据中的退化信息压缩为统一的任务级先验。其核心设计思路是：同类退化（如不同强度的雨纹）在特征空间中具有明显的类内聚集性，而不同类退化（如雨与雾）则表现出类间可分性。融合器利用干净目标图像作为引导，将每种退化类型的类内特征聚合为一个紧凑的表示向量，所有任务的表示共同构成退化知识银行（Degradation Bank）。

银行中每个条目包含一对键-值特征：键用于后续的退化匹配，值则存储该退化类型对应的干净先验信息。银行容量由超参数$M$控制——消融实验（Table 5）表明，在三退化任务下$M=64$即可达到最佳平均PSNR（32.53 dB），继续增大$M$不再带来明显增益。

### 退化匹配与先验检索

在推理阶段，退化匹配模块负责将输入退化图像的特征与银行中的键进行全局匹配，检索出最相关的干净先验。具体流程如下：

**第一步：全局相似度计算。** 将退化查询特征$\boldsymbol{D}_{\boldsymbol{K}} \in \mathbb{R}^{B \times H \times W \times C_k}$与银行中所有任务的键矩阵$\boldsymbol{U}_{\boldsymbol{K}}$进行矩阵乘法，得到全局相似度矩阵：

$$\boldsymbol{S} = \boldsymbol{D}_{\boldsymbol{K}} \times \boldsymbol{U}_{\boldsymbol{K}}^{T}$$

其中$B$为批次大小，$H \times W$为空间维度，$C_k$为键通道数。

**第二步：局部平均与任务选择。** 对相似度矩阵$\boldsymbol{S}$沿空间维度进行局部平均（Local-Mean），然后通过Argmax操作选出与当前输入最匹配的任务类别，并对其他任务进行掩码屏蔽：

$$S_{mask} = \mathrm{Mask}(\mathrm{Argmax}(\mathrm{Local\text{-}Mean}(S)))$$

这一全局匹配策略确保每个退化样本仅与其最相关的任务级先验进行交互，避免了多任务间的特征干扰。

**第三步：门控卷积融合。** 检索到的值特征$\boldsymbol{U}_{\boldsymbol{V}}$经Softmax加权后，与查询特征$\boldsymbol{D}_{\boldsymbol{V}}$通过通道交叉级联（channel-interleaved concatenation）拼接，再送入门控卷积模块生成最终的锐化先验$\boldsymbol{S}_{\boldsymbol{V}}$：

$$S_{V} = \mathtt{Gate\text{-}Conv}(U_{V} \times \mathtt{Softmax}(S_{mask}), D_{V})$$

其中Gate-Conv实现为$3 \times 3$分组卷积，分组数等于值通道数$C_v$。这一设计确保每个退化样本仅与检索到的对应先验进行通道级交互，避免了不同样本之间的先验污染。融合后的锐化先验$\boldsymbol{S}_{\boldsymbol{V}}$被注入到解码器的最底层，逐级向上指导特征重建。

### 多损失联合优化

R2R采用端到端训练，无需多阶段优化。总损失函数由四项组成：

$$\mathcal{L} = \mathcal{L}_{pixel} + \lambda_{d} \cdot \mathcal{L}_{deg} + \lambda_{m} \cdot \mathcal{L}_{match} + \lambda_{f} \cdot \mathcal{L}_{fft}$$

各分量含义如下：
- **$\mathcal{L}_{pixel}$**：像素域L1重建损失，作用于恢复图像与干净目标之间；
- **$\mathcal{L}_{deg}$**：退化分类损失，监督退化融合器正确识别退化类型（权重$\lambda_d=0.1$）；
- **$\mathcal{L}_{match}$**：匹配损失，确保退化匹配模块检索到正确的任务先验（权重$\lambda_m=0.1$）；
- **$\mathcal{L}_{fft}$**：频域L1损失，在傅里叶域对恢复图像与干净图像施加约束：

$$\mathcal{L}_{fft} = \frac{1}{P} || \mathcal{F}(\hat{x}) - \mathcal{F}(x) ||_{1}$$

其中$\mathcal{F}(\cdot)$表示快速傅里叶变换，$P$为像素总数，权重$\lambda_f=0.125$。频域损失的引入有效提升了高频细节（如纹理、边缘）的保真度。

消融实验（Table 6）验证了各损失分量的贡献：在基础像素损失上依次添加频域损失、退化分类损失和匹配损失，累计带来0.65 dB的平均PSNR提升。

### 结构设计要点

共享重建主干采用对称的四层U型编码器-解码器结构，基于**NAFBlock**（Chen et al., NeurIPS 2022）构建。编码器各层NAFBlock数量从上到下依次为[1, 1, 1, 28]，解码器对称配置。这种轻量级设计使得R2R仅需19.7M参数和12G MACs（224×224输入），相比**PromptIR**（Potlapalli et al., NeurIPS 2023）的132G MACs减少了约91%，同时实现了更优的恢复质量。

### 补充图表

![[assets/figures/papers/paper_list_l925_https_openaccess_thecvf_com_content_CVPR2026_html_Wang_Retrieve_to_Resto/figures/009_Figure_6.jpg]]
*Figure 6: t-SNE visualization of*



## 实验与关键发现

### 实验设置

R2R采用对称的四层编码器-解码器架构，编码器各级NAFBlock数量为[1, 1, 1, 28]，解码器为[1, 1, 1, 2]。退化融合器包含三个卷积阶段，退化匹配模块的键特征通道数$C_k=8$，值特征通道数$C_v=64$。训练使用AdamW优化器，初始学习率$2\times10^{-4}$，余弦退火调度，总损失权重$\lambda_d=0.1$、$\lambda_m=0.1$、$\lambda_f=0.125$。所有对比方法均采用公开预训练权重或严格按原论文设置复现，计算复杂度统一在224×224输入分辨率上使用NVIDIA RTX 5090 GPU测量。

### 三退化一体化恢复

Table 1展示了在去雾（SOTS）、去雨（Rain100L）、去噪（BSD68, σ=15/25/50）三个任务上的综合对比。R2R以平均**32.53 dB PSNR / 0.918 SSIM**取得最优，较**PromptIR**（Potlapalli et al., NeurIPS 2023）提升0.47 dB，而计算量仅为其约9%（12G vs 132G MACs）。具体而言，R2R在SOTS去雾上达到31.40 dB，Rain100L去雨上达到37.46 dB，去噪任务（σ=15/25/50）分别为33.98/31.25/29.18 dB。值得注意的是，R2R在去噪中等噪声强度（σ=25）上略低于Gridformer（31.25 vs 31.36 dB），但整体平均性能最优，验证了检索式退化先验在参数效率上的显著优势。

### 五退化一体化恢复

当退化类型扩展至五种（增加GoPro去模糊和LOL低光增强）时（Table 2），R2R仍以**30.48 dB平均PSNR**领先，较**AirNet**（Li et al., CVPR 2022）提升约4.44 dB，较**Perceive-IR**（Zhang et al., IEEE TIP 2025）提升2.18 dB。尤其在低光增强任务上，R2R达到24.36 dB，显著优于多数专用一体化方法，表明退化银行中存储的统一先验对光照退化同样具备有效引导能力。

![[assets/figures/papers/paper_list_l925_https_openaccess_thecvf_com_content_CVPR2026_html_Wang_Retrieve_to_Resto/figures/004_Table_2.jpg]]
*Table 2: Comparison to state-of-the-art on five degradations. PSNR (dB, ↑) and SSIM (↑) metrics are reported on the full RGB images with (∗) denoting general image restorers, others are specialized all-in-one approaches. Best and second best performances are highlighted*

### 单退化任务表现

Table 3进一步验证了R2R在单退化场景下的竞争力。在SOTS去雾上达到**31.50 dB**，超过Gridformer（30.37 dB）1.13 dB；在Rain100L去雨上达到**37.45 dB**，超过Restormer（36.67 dB）0.78 dB。这证明即使不依赖多任务联合训练的优势，检索式先验注入机制本身即可有效提升单任务恢复质量。

### 任务鲁棒性分析

Figure 3揭示了各方法在退化类型递增时的性能衰减模式。从单任务过渡到三任务联合训练时，R2R在去雾、去雨、去噪上的PSNR降幅均在**0.5 dB以内**，而Gridformer和PromptIR的降幅普遍超过1.5 dB。从三任务扩展至五任务时（Figure 3(d)），R2R的额外损失同样最小。这一结果直接验证了核心因果机制：将退化知识外置为独立先验，有效缓解了共享主干网络中的参数专业化冲突，使模型在多任务扩展时保持优化稳定性。

![[assets/figures/papers/paper_list_l925_https_openaccess_thecvf_com_content_CVPR2026_html_Wang_Retrieve_to_Resto/figures/006_Figure_3.jpg]]
*Figure 3: Task robustness of R2R and state-of-the-art methods as the number of degradation types increases. (a)–(c) denote the performance change from single-task dehazing, deraining, and denoising to the three-task setting; (d) denotes the extension from three-task to five-task restoration*

### 计算效率与复杂度

Table 4的复杂度分析显示，R2R在224×224输入下参数量**19.7M**，推理内存**846 MB**，MACs仅**12G**。相比之下，PromptIR需132G MACs（约11倍），Gridformer需251G MACs（约21倍）。即使与轻量级通用恢复器**InstructIR**（Conde et al., ECCV 2024）的44G MACs相比，R2R仍节省约73%计算量。这种效率优势源于退化匹配模块仅在编码器最低层执行一次检索-融合操作，避免了主干网络内部持续的退化条件调制开销。

### 消融实验

**退化银行容量M**（Table 5）：当M从16增至64时，平均PSNR从32.07 dB持续提升至32.53 dB；M=128时性能持平（32.52 dB），表明M=64已能充分覆盖三类退化的任务级先验空间，继续增大不再带来增益。

**损失函数贡献**（Table 6）：在基础L1像素损失（$\mathcal{L}_{pixel}$）上逐步添加退化分类损失（$\mathcal{L}_{deg}$）、匹配损失（$\mathcal{L}_{match}$）和频域损失（$\mathcal{L}_{fft}$），累计带来**0.65 dB平均PSNR增益**。其中频域损失单独贡献约0.3 dB，对高频细节恢复尤为关键。

**退化银行对HQ数据的依赖性**（Table 7）：使用低质量（LQ）图像替代干净HQ图像构建退化银行时，平均PSNR仅从32.53 dB降至**32.33 dB**（-0.2 dB）。这表明退化融合器学习的任务级先验对输入质量不敏感，降低了方法对高质量配对数据的依赖，增强了实际部署的可行性。

### 失败模式与局限性

尽管R2R在离散退化类型上表现优异，但存在以下局限：

1. **退化银行需预定义类型**：无法直接处理完全未知的新退化类别，扩展新任务需重新训练退化融合器并更新银行。
2. **混合退化支持不足**：当前匹配机制假设输入属于单一退化类型，对雨雾共存等混合退化场景缺乏显式建模。
3. **银行容量与任务数耦合**：当退化类型持续增加时，M可能需要重新调整，检索效率可能成为瓶颈。
4. **仍依赖配对数据**：虽然银行可由LQ图像构建，但训练阶段仍需访问配对数据（或伪配对数据）以学习退化分类和匹配信号。

### 补充图表

![[assets/figures/papers/paper_list_l925_https_openaccess_thecvf_com_content_CVPR2026_html_Wang_Retrieve_to_Resto/figures/001_Figure_1.jpg]]
*Figure 1: Comparison of average PSNR and computational cost (MACs) across different methods. Our method achieves a 0.47dB PSNR improvement while reducing MACs by approximately 91% compared to PromptIR [38]*

![[assets/figures/papers/paper_list_l925_https_openaccess_thecvf_com_content_CVPR2026_html_Wang_Retrieve_to_Resto/figures/003_Table_1.jpg]]
*Table 1: Comparison to state-of-the-art on three degradations. PSNR (dB, ↑) and SSIM (↑) metrics are reported on the full RGB images. Best and second best performances are highlighted. Our method sets a new state-of-the-art on average across all benchmarks while being significantly more efficient than prior work. ‘-’ represents unreported results*

![[assets/figures/papers/paper_list_l925_https_openaccess_thecvf_com_content_CVPR2026_html_Wang_Retrieve_to_Resto/figures/005_Table_3.jpg]]
*Table 3: Comparison to state-of-the-art for single degradations. PSNR (dB, ↑) and SSIM (↑) metrics are reported on the full RGB images. Best and second best performances are highlighted. Our method excels prior work on dehazing and deraining*

![[assets/figures/papers/paper_list_l925_https_openaccess_thecvf_com_content_CVPR2026_html_Wang_Retrieve_to_Resto/figures/008_Table_4.jpg]]
*Table 4: Complexity Analysis. MACs are computed on an input image of size 224 × 224 using a NVIDIA RTX 5090 (32G) GPU. ∗ denotes patch size of 512 × 512*

![[assets/figures/papers/paper_list_l925_https_openaccess_thecvf_com_content_CVPR2026_html_Wang_Retrieve_to_Resto/figures/010_Table_5.jpg]]
*Table 5: Ablation study of the Hyperparameter M under the 3- degradation task. The average PSNR and SSIM are reported*

![[assets/figures/papers/paper_list_l925_https_openaccess_thecvf_com_content_CVPR2026_html_Wang_Retrieve_to_Resto/figures/012_Table_6.jpg]]
*Table 6: Effectiveness of the different loss functions under the 3- degradation task. (a), (b), (c), (d) denote*

![[assets/figures/papers/paper_list_l925_https_openaccess_thecvf_com_content_CVPR2026_html_Wang_Retrieve_to_Resto/figures/013_Table_7.jpg]]
*Table 7: Results on HQ dependence in the Degradation Bank (DB)*

![[assets/figures/papers/paper_list_l925_https_openaccess_thecvf_com_content_CVPR2026_html_Wang_Retrieve_to_Resto/figures/007_Figure_4.jpg]]
*Figure 4: Visual comparison of R2R with state-of-the-art methods considering three degradations. Zoom in for a better view*



## 定位与知识库关联

### 1. 核心问题与因果机制

一体化图像恢复（All-in-One Image Restoration）的核心瓶颈在于：当多种退化类型（如雾、雨、噪声、模糊、低光）在共享主干网络中联合训练时，不同任务的参数更新方向存在冲突，导致**参数专业化冲突**和优化不稳定，严重制约了模型性能上限。现有方法试图通过内部调制机制来解决这一问题，但本质上是“在冲突的战场上调解”，而非“将冲突方分离”。

R2R 的核心因果操控是：**将退化知识从共享主干中彻底解耦**。具体而言，R2R 放弃了内部提示（如 **PromptIR**，Potlapalli et al., NeurIPS 2023）、MoE 路由（如 **Gridformer**，Wang et al., IJCV 2024）等将退化线索嵌入主干内部的方案，转而采用**外部检索式退化知识库**（Degradation Bank），在主干网络的最低层通过退化匹配模块注入任务级先验，使主干仅承担与任务无关的共享重建功能。

这一设计的深层洞察是：不同退化类型（雨纹、雾、噪声等）在特征空间中表现出明显的**类内相似性和类间可分性**，因此可以用紧凑的统一任务级先验来表示。推理时按需检索相关先验来调节卷积特征，从而在轻量级共享主干上实现稳定、高效的多退化恢复。

### 2. 与现有方法的谱系关系

#### 2.1 任务特定恢复方法

在单任务恢复领域，**MPRNet**（Zamir et al., CVPR 2021）采用多阶段渐进式架构，**NAFNet**（Chen et al., NeurIPS 2022）以简化的非线性激活单元实现高效去模糊和去噪。R2R 直接以 NAFNet 的 U 形编码器-解码器作为共享主干，但将其从“任务特定”扩展为“任务无关”的共享重建模块。在单退化设定下，R2R 在去雾（SOTS: 31.50 dB）和去雨（Rain100L: 37.45 dB）上均超越了包括 **Restormer** 在内的专用方法（Table 3），证明解耦设计并未损害单任务性能。

#### 2.2 基于内部调制的一体化方法

这是 R2R 最直接的对比谱系：

- **PromptIR**（Potlapalli et al., NeurIPS 2023）：通过视觉提示（prompts）在主干内部注入退化信息，三任务平均 PSNR 为 32.06 dB，但计算量高达 132G MACs。R2R 在相同设定下达到 32.53 dB，MACs 仅 12G（减少约 91%）。
- **AirNet**（Li et al., CVPR 2022）：基于对比学习分离退化与内容表征，五任务平均 PSNR 约 26.04 dB，R2R 达到 30.48 dB（+4.44 dB），且计算量更低。
- **Gridformer**（Wang et al., IJCV 2024）：基于 Transformer 的多天气恢复，单任务去雾 30.37 dB，R2R 达到 31.50 dB（+1.13 dB）。
- **InstructIR**（Conde et al., ECCV 2024）：利用人类指令引导恢复，属于高层语义调制范式。
- **Perceive-IR**（Zhang et al., IEEE TIP 2025）：面向退化感知的设计，关注退化类型的识别与适应。

R2R 与上述方法的根本差异在于**退化适应机制的“内-外”之辨**：内部调制方法将退化信息作为主干的一部分参与所有层的特征变换，导致参数更新冲突；R2R 将退化知识外置为可检索的先验，在最低层一次性注入，主干各层仅处理共享的“纯净”特征变换。这一差异在任务鲁棒性实验中体现得尤为明显（Figure 3）：当退化类型从 1 种增加到 3 种再到 5 种时，R2R 的 PSNR 降幅在 0.5 dB 以内，远小于 Gridformer、PromptIR 等方法，证明参数冲突得到了有效缓解。

#### 2.3 检索增强与知识库方法

R2R 的“检索即恢复”范式与检索增强生成（RAG）在思想上相通，但在图像恢复领域具有独创性。退化银行（Degradation Bank）的构建方式也区别于传统方法：传统先验构建通常依赖干净目标图像（HQ），而 R2R 的消融实验（Table 7）表明，用低质量图像（LQ）构建退化银行仅比 HQ 构建损失 0.2 dB（32.33 vs 32.53），证明该方法对高质量数据的依赖性较低，这一特性在现实场景中具有重要实用价值。

### 3. 适用边界与局限

尽管 R2R 在效率和多任务鲁棒性上表现突出，但其设计存在明确的适用边界：

1. **退化类型需预定义**：退化银行的构建需要预先知道退化类别（雾、雨、噪声等），无法直接处理完全未知的新退化类型。当遇到银行中不存在的退化时，匹配模块可能将其错误映射到最相似类别，导致次优恢复。

2. **离散退化假设**：R2R 目前仅支持离散的退化类型，对混合退化（如同时存在雾和噪声）或连续退化强度（如噪声水平 σ 的连续变化）的直接支持尚不明确。虽然银行中的先验可以包含一定程度的类内变化，但论文未系统验证混合退化场景。

3. **银行容量的可扩展性**：超参数 M（银行容量）在 M=64 时达到最优（Table 5），继续增大不再带来明显提升。但当退化类型持续增加时（如从 5 种扩展到 10 种以上），银行容量可能需要重新调整，检索效率也可能成为瓶颈——当前采用全局匹配方案，未使用近似检索加速。

4. **配对数据依赖**：尽管银行可由低质量图像构建，但退化融合器（Degradation Amalgamator）的训练仍需访问配对数据（或伪配对数据）来学习退化特定的统一先验。在完全无监督设置下，如何构建和训练退化银行仍是开放问题。

### 4. 开放问题与未来方向

基于 R2R 的设计逻辑和当前局限，以下方向值得探索：

1. **动态退化与视频恢复**：如何将检索式先验扩展到视频恢复或动态退化场景？视频中的退化可能随时间变化，需要在线更新检索策略或引入时序一致性约束。

2. **无监督/自监督扩展**：在完全无监督或自监督学习设置下，退化匹配和银行构建策略如何调整？是否可以利用对比学习或聚类自动发现退化类别并构建先验？

3. **语义级先验增强**：是否可以利用视觉-语言模型（如 CLIP）提供更高层次的语义先验，以增强退化匹配的泛化能力？例如，文本描述“雾天场景”可以作为额外的匹配线索。

4. **大规模退化银行的检索效率**：当退化银行中存储大量类别（如数十种）时，全局匹配的计算成本可能成为瓶颈。采用近似最近邻检索（ANN）或分层匹配策略是自然的扩展方向。

5. **生成式恢复的结合**：检索到的先验目前用于调节卷积特征，能否将其注入扩散模型或生成式恢复框架，在保持效率的同时提升感知质量？这需要平衡检索先验的确定性引导与生成模型的多样性。



## 原文 PDF

![[paperPDFs/CVPR_2026/Retrieve_to_Restore_Efficient_All_in_One_Image_Restoration_with_a_Retrieval_Based_Degradation_Bank.pdf]]

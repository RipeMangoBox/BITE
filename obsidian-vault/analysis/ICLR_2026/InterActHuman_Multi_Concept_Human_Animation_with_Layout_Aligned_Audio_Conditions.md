---
title: "InterActHuman: Multi-Concept Human Animation with Layout-Aligned Audio Conditions"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/InterActHuman_Multi_Concept_Human_Animation_with_Layout_Aligned_Audio_Conditions.pdf
project_link: https://zhenzhiwang.github.io/interacthuman/
code_link: null
openreview_forum_id: rJilRU8D3c
aliases:
- InterActHuman
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: "在扩散Transformer中引入显式的掩码预测分支，通过迭代缓存和交错的掩码预测策略实现音频条件的局部注入，打破条件全局注入的鸡与蛋困局。"
primary_logic: "通过在去噪过程中从含噪视频特征自动预测各身份的空间布局，并使用上一步的掩码指导下一步的本地音频注入，模型能够在无真实布局的情况下实现精确的多身份同步动画。"
claims:
- "在消融实验中，使用预测动态掩码的本地音频注入显著优于全局音频和固定掩码，在Sync-D和FVD上均取得最佳性能。"
- "所提出的交错掩码预测策略解决了推理时无法获取真实布局的问题，通过上一步的预测掩码引导当前步的条件注入。"
- "在用户偏好研究中，我们的方法在音频驱动多说话人视频和多人概念定制两个任务上均获得最高平均分和Top-1选择率。"
- "Multi-Person Audio-Driven Test Set 上 FVD (↓) = 22.881"
---

# InterActHuman: Multi-Concept Human Animation with Layout-Aligned Audio Conditions

> [!tip] 核心洞察
> 通过在去噪过程中从含噪视频特征自动预测各身份的空间布局，并使用上一步的掩码指导下一步的本地音频注入，模型能够在无真实布局的情况下实现精确的多身份同步动画。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | InterActHuman：基于布局对齐音频条件的多概念人体动画 |
| 英文题名 | InterActHuman: Multi-Concept Human Animation with Layout-Aligned Audio Conditions |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=rJilRU8D3c) · [Project](https://zhenzhiwang.github.io/interacthuman/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | InterActHuman |
| Dataset | Multi-Person Audio-Driven Test Set, Multi-Concept Video Customization Test Set |

> [!tip] 效果简介
> - Multi-Person Audio-Driven Test Set 上，FVD (↓) 为 22.881，对比 33.555 (Kling1.6+Lip-sync)，变化 -10.674。
> - Multi-Person Audio-Driven Test Set 上，Sync-D (↓) 为 6.670，对比 7.068 (OmniHuman w/ fixed mask)，变化 -0.398。
> - Multi-Concept Video Customization Test Set 上，CLIP-I (↑) 为 0.744，对比 0.703 (Phantom*)，变化 +0.041。

## 概要

### 问题与瓶颈

多概念人体动画任务要求根据多个参考身份的外观和各自的音频输入，生成一段同步、自然的视频。现有方法普遍采用**全局条件注入**策略，即将所有音频信号不加区分地注入到全部视频令牌中。这在多说话人场景下会引发严重的**音频-身份错位**：模型无法判断哪段音频应驱动哪个人物，导致唇同步混乱、身份混淆。此瓶颈的本质在于缺乏一个显式的**时空布局绑定机制**，使得音频条件与视觉区域之间的对应关系只能通过注意力机制隐式学习，而这种隐式学习在多身份、重叠场景下极易失效。

### 核心方法

**InterActHuman** 的核心洞察是：**在扩散去噪过程中，从含噪视频特征中自动预测各身份的空间布局掩码，并利用上一步的掩码指导当前步的本地音频注入**，从而打破条件全局注入的“鸡与蛋”困局。

具体而言，该方法在扩散Transformer（DiT）中引入一个轻量级的**掩码预测分支**（跨注意力 + MLP），为每个参考身份预测逐层的时空掩码。推理时采用**交错掩码预测策略**：第 $k$ 步预测的掩码被缓存，并在第 $k+1$ 步用于指导音频条件的局部注入——仅对掩码区域内的令牌注入对应身份的音频特征，其余区域则注入静音特征。这一设计使模型在**无需真实布局标注**的情况下，实现了精确的多身份同步动画。

### 方法定位

InterActHuman 在方法谱系中处于**扩散Transformer + 显式布局引导**的交叉点。与 OmniHuman（Lin et al., 2025a）等全局条件注入方法相比，其关键差异在于将音频条件从“全局广播”改为“局部绑定”；与 MultiTalk 等多人物说话头方法相比，它不依赖预定义的人脸检测或裁剪，而是通过端到端学习的掩码预测器自动推断布局。该方法还兼容多概念视频定制任务，将参考图像的外观注入与布局对齐的音频注入统一在同一框架下。

### 主要结果

在**多人物音频驱动测试集**上，InterActHuman 取得了 **FVD 22.881**（较 Kling1.6+Lip-sync 的 33.555 降低 10.674）和 **Sync-D 6.670**（优于 OmniHuman 固定掩码变体的 7.068）。在**多概念视频定制测试集**上，CLIP-I 达到 **0.744**（Phantom* 为 0.703），DINO-I 达到 **0.533**（Phantom* 为 0.476）。用户偏好研究中，本方法在音频驱动任务上获得平均分 **2.48**（OmniHuman 为 1.82），在多概念定制任务上获得 **4.01**（Vidu2.0 为 3.40），Top-1 选择率分别为 **59.9%** 和 **49.4%**，均显著领先。

消融实验进一步证实：预测动态掩码的本地音频注入在 Sync-D（6.670）和 FVD（22.881）上均显著优于全局音频（9.482, 33.895）和固定掩码（7.068, 40.239）；掩码缓存策略将多说话人唇同步 Sync-D 从 11.046 提升至 6.921。掩码预测分支仅增加 **56M 参数**，每额外参考图像仅增加 **0.4 秒**推理时间，开销极小。

### 局限与开放问题

当前方法的掩码预测在多人物严重重叠时可能不准确，且掩码质量受限于 VAE 的低分辨率潜在空间。训练数据以 2-3 人对话场景为主，向更多人数扩展时虽性能稳定，但尚未充分优化。此外，模型依赖于 T2V 先验，当文本提示与训练分布偏差较大时可能产生不自然内容。开放问题包括：如何改进掩码预测以处理高重叠区域、如何缓解低分辨率潜在空间带来的边界精度损失，以及能否将布局条件绑定扩展到文本等其他模态。



### 问题背景

音频驱动的人体动画旨在根据语音信号生成逼真的人物视频，使其口型、表情和肢体动作与音频内容同步。近年来，扩散模型在该领域取得了显著进展，涌现出**DiffTED**（Hogue et al., 2024）、**DiffGest + Mimiction**（Zhu et al., 2023; Zhang et al., 2024）、**CyberHost**（Lin et al., 2024）以及**OmniHuman**（Lin et al., 2025a）等方法。然而，这些工作主要聚焦于**单人场景**——即给定一段音频和一张参考人物图像，生成该人物说话的视频。

现实应用往往需要处理更复杂的**多概念人体动画**场景：多个说话人交替或同时发声，每个说话人拥有独立的身份外观和音频轨道。这种场景对模型提出了双重挑战：既要保持每个身份的外观一致性，又要确保每个身份的口型仅与其对应的音频片段同步，而非被其他说话人的音频干扰。

### 现有方法的瓶颈：全局条件注入的“鸡与蛋”困局

现有多概念人体动画方法的核心缺陷在于**全局条件注入**机制。以OmniHuman为代表的方案将音频特征作为全局条件注入扩散Transformer的所有视频令牌，这意味着整个视频帧中的所有区域都受到同一音频信号的影响。在多说话人场景下，这种设计导致一个根本性问题：模型无法区分“谁在说话”，因此音频条件会错误地驱动所有身份的口型运动，造成**音频与说话人的错误对齐**。

从因果机制来看，这形成了一个“鸡与蛋”的困局：
- 要实现精确的局部音频绑定，模型需要知道每个身份在视频帧中的**空间布局**（即哪个区域属于哪个说话人）；
- 但在生成过程中，这种布局信息本身是未知的，需要从去噪过程中的中间结果推断；
- 如果没有布局引导，全局注入的音频条件又会进一步模糊身份区域的区分，使布局推断更加困难。

这一瓶颈在**多说话人唇同步**任务上表现尤为突出。消融实验（Table 4）显示，全局音频注入方案的Sync-D指标高达9.482，而引入显式布局对齐后降至6.670，差距显著。

### 本文动机与核心思路

InterActHuman的动机在于打破上述困局：**在扩散Transformer中引入显式的掩码预测分支，使模型能够在去噪过程中自动推断各身份的空间布局，并利用该布局实现音频条件的局部注入**。

核心洞察可以概括为：通过从含噪视频特征中预测每个参考身份的时空掩码，并将上一步的预测掩码缓存用于指导下一步的本地音频注入，模型可以在**无需真实布局标注**的情况下实现精确的多身份同步动画。这一设计将布局推断与条件注入解耦为两个交替进行的子任务，使模型能够通过迭代优化逐步收敛到准确的音频-身份绑定。

具体而言，InterActHuman在两个方面改变了现有范式的条件注入方式：
- **音频条件注入方式**：从全局注入（所有视频令牌均受音频影响）转变为局部注入，仅对掩码预测区域内的令牌注入对应身份的音频特征（Section 3.2）；
- **布局控制机制**：从隐式学习条件与区域的对应关系（通过注意力机制）转变为显式预测逐身份时空掩码，并跨扩散步缓存迭代优化。

通过这一设计，InterActHuman不仅能够处理多说话人对话场景，还支持多概念定制（如人物换装、人-物交互、动漫风格等），实现了统一的音频驱动多概念生成框架。



## 核心方法与创新机理

InterActHuman 的核心创新在于**为扩散Transformer引入了显式的布局感知音频注入机制**，从根本上解决了现有多概念人体动画方法中音频条件全局注入导致的身份绑定错误问题。

### 问题根源：全局条件注入的“鸡与蛋”困局

现有方法（如 **OmniHuman** (Lin et al., 2025a)）将音频特征作为全局条件注入所有视频令牌，模型通过注意力机制隐式学习音频与说话人的对应关系。在多说话人场景下，这种全局注入策略缺乏精确的时空绑定，导致音频与说话人错误对齐——模型需要知道“谁在说话”才能正确分配音频，但这一信息本身又依赖于音频注入的结果。InterActHuman 通过**显式的布局预测**打破这一循环。

### 关键机制：从全局注入到布局对齐的局部注入

InterActHuman 在三个关键维度上对基线方法进行了根本性改造：

**1. 音频条件注入方式：全局 → 局部**

基线方法（如 OmniHuman）将 wav2vec 音频特征作为全局条件注入所有视频令牌，所有空间位置均受音频影响。InterActHuman 改为**局部注入**：仅对掩码预测区域内的令牌注入对应身份的音频特征，非说话人区域使用静音音频特征填充。这一改造直接切断了音频条件对无关区域的干扰，使唇同步精度在多说话人场景下显著提升——消融实验显示，局部注入的 Sync-D 达到 6.670，远优于全局注入的 9.482（Table 4）。

**2. 布局控制机制：隐式学习 → 显式掩码预测**

基线方法依赖注意力机制的隐式学习来建立条件与区域的对应关系，缺乏可监督的布局信号。InterActHuman 引入了**轻量化掩码预测分支**（跨注意力 + MLP），为每个参考图像显式预测逐帧时空掩码，量化该身份在视频各帧各空间位置的出现强度。该掩码预测器仅增加约 56M 参数（相对于 7B 的 DiT 主干），每参考图像仅增加约 0.4 秒推理开销（Table 5），但带来了显著的性能增益。

**3. 条件注入架构：统一全局处理 → 模态分离处理**

基线方法对所有模态（图像、文本、音频）采用统一的全局处理方式。InterActHuman 采用**模态分离策略**：图像和文本等全局模态沿用原有的自注意力注入；音频作为局部模态，通过预测掩码绑定到特定身份区域。这一分离设计使模型既能保持全局外观一致性，又能实现精确的局部音频驱动。

### 推理时的交错掩码预测策略

训练时掩码预测器使用 Grounding-SAM2 生成的伪真值掩码进行监督。然而推理时无法获取真实布局，InterActHuman 提出了**交错掩码预测策略**：在去噪过程中，第 k 步预测的掩码被缓存，并在第 k+1 步作为布局先验指导音频条件的局部注入。这一策略使模型在无真值布局的情况下仍能实现精确的多身份同步动画。消融实验证实，使用缓存掩码使多说话人唇同步的 Sync-D 从 11.046 大幅改善至 6.921（Table 12）。

### 创新效果验证

消融实验（Table 4）系统验证了上述创新的有效性：
- **预测动态掩码**在 FVD 上达到 22.881，显著优于固定掩码（40.239）和全局音频（33.895），表明显式布局预测能提升视频质量与时间一致性；
- **预测动态掩码**在 Sync-D 上达到 6.670，优于全局音频（9.482）和 ID 嵌入（8.627），验证了布局对齐对唇同步的关键作用；
- 用户偏好研究中，InterActHuman 在音频驱动多说话人视频和多人概念定制两个任务上均获得最高平均分（2.48 和 4.01）及最高 Top-1 选择率（59.9% 和 49.4%）（Table 2）。

### 失败模式与局限

当多人物重叠严重时，掩码预测可能不准确，导致音频分配错误（Figure 5）。此外，掩码质量受限于预训练 VAE 的低分辨率潜在空间，可能影响边界精度。当前训练数据主要为 2-3 人的对话场景，扩展到更多人数时虽性能稳定（Table 13），但尚未针对更大规模进行优化。



![[assets/figures/papers/paper_list_l15_https_openreview_net_forum_id_rJilRU8D3c/figures/002_Figure_2.jpg]]
*Figure 2: Illustration of our framework, which adaptively predicts masks as the spatial guidance of audio condition injection. In training, we train the mask predictor (cross-attn w/ MLP) with mask loss; in inference, we collect mask predictions to cache and leverage masks predicted from the last denoising step (t − 1) to guide the audio cross-attn in the current denoising step (t)*

![[assets/figures/papers/paper_list_l15_https_openreview_net_forum_id_rJilRU8D3c/figures/001_Figure_1.jpg]]
*Figure 1: Video frames generated from audio and multi-concept reference images (human heads/full bodies, objects, scenes) display rich, audio-matched expressions. Our method enables compositional generation including outfit changes, human–object interactions, anime styles, dialogues even without a start frame. Red and green wave icons denote speaking and listening, respectively*

InterActHuman 的整体 pipeline 围绕一个核心因果机制构建：**在扩散 Transformer 的去噪过程中，通过显式预测各身份的空间布局掩码，打破条件全局注入的“鸡与蛋”困局，实现音频与说话人的精确时空绑定**。

### 输入与输出流

框架接收三类输入：多概念参考图像（可包含人头、全身、物体等）、对应的音频流（含多说话人语音）以及可选的文本提示。输出为一段多概念人体动画视频，其中每个身份的口型和肢体动作与其对应的音频片段精确同步。

### 核心模块与数据流

pipeline 由五个关键模块串联构成，数据流遵循“压缩→去噪→掩码预测→局部条件注入→解码”的路径：

1.  **VAE Encoder/Decoder**：首先利用 3D VAE 将输入视频压缩至低维潜在空间，扩散过程在该空间中执行；生成完成后，VAE Decoder 将潜在表示解码回像素空间视频。

2.  **DiT Backbone（基于 MMDiT 的视频生成模型）**：作为主干网络，负责迭代去噪。参考图像的外观信息通过自注意力机制注入到 DiT 层的视频令牌中，实现多概念外观的定制化生成。

3.  **Mask Predictor（掩码预测器）**：这是框架的核心创新模块。它是一个轻量化的跨注意力 + MLP 结构，附加在 DiT 的每一层 Transformer 上。对于每个参考图像，该模块从去噪过程中的视频特征出发，通过跨注意力计算视频令牌与参考图像特征之间的相似度，再经 MLP 和 Sigmoid 激活，预测出一个时空掩码 $m_i^{(l)}$，量化该参考图像在每一帧视频中应占据的空间区域。

4.  **Audio Conditioning Module（音频条件注入模块）**：在每个 DiT 块中新增跨注意力层，负责将 wav2vec 音频特征注入视频令牌。与全局注入不同，该模块仅对掩码预测器所指定的区域注入对应身份的音频特征，实现局部条件绑定：
    $$
    \mathbf{h}^v \gets \mathbf{h}^v + m_i \odot \mathbf{p}_i + (1 - m_i) \odot \mathbf{p}_i^{\mathrm{mute}}
    $$
    其中 $\mathbf{p}_i$ 为说话音频特征，$\mathbf{p}_i^{\mathrm{mute}}$ 为静音特征，$m_i$ 为预测掩码。

5.  **Iterative Mask Caching and Injection（迭代掩码缓存与注入）**：推理时的关键策略。由于推理过程无法获取真实布局，框架采用交错预测机制——**第 $k$ 步去噪预测出的掩码被缓存，并在第 $k+1$ 步作为布局先验，指导音频条件注入**。这打破了“需要掩码才能注入音频，但掩码又依赖去噪结果”的死循环。

### 训练与推理分离的设计逻辑

-   **训练阶段**：掩码预测器使用 Grounding-SAM2 提取的真实时空掩码作为监督信号，训练损失由 Flow Matching 扩散损失和掩码分类的 Focal Loss 联合构成。
-   **推理阶段**：无需真实掩码，完全依赖上一步的预测掩码进行迭代引导。消融实验证实，这一缓存策略使多说话人唇同步指标 Sync-D 从 11.046 显著改善至 6.921（Table 12）。

### 条件注入的分离策略

框架对不同模态的条件采取了差异化的注入方式：
-   **全局模态**（参考图像、文本）：沿用 DiT 原有的全局自注意力机制，确保整体外观一致性和文本跟随。
-   **局部模态**（音频）：通过预测掩码绑定到特定身份区域，仅在掩码覆盖的视频令牌中注入对应音频特征，避免多说话人场景下的音频串扰。

这种设计使得模型在无需真实布局标注的情况下，能够自动推断各身份的空间位置，并据此精确分配音频条件。消融实验（Table 4）表明，预测动态掩码在 Sync-D（6.670）和 FVD（22.881）上均显著优于全局音频注入（Sync-D 9.482, FVD 33.895）和固定掩码（Sync-D 7.068, FVD 40.239），验证了显式布局对齐对唇同步和视频质量的关键作用。掩码预测器的开销极小（仅增加 56M 参数，每额外参考图像增加约 0.4 秒推理时间），但带来了显著的性能提升。



### 整体架构

InterActHuman以基于MMDiT的视频生成扩散Transformer为主干，在其上附加两个关键模块：**掩码预测器**与**局部音频条件注入**。框架的核心创新在于将布局预测与条件注入解耦为交错执行的两个子任务，从而打破“需要布局才能注入条件，但布局又依赖于生成结果”的鸡与蛋困局。

### 基础扩散目标

模型采用Flow Matching训练范式。给定干净潜在表示 $z_0$、噪声 $\epsilon$ 和时间步 $t$，含噪潜在表示为 $z_t$，训练目标为预测速度场：

$$\mathcal{L} = \mathbb{E}_{t, z_0, \epsilon} \left\| v_\Theta(z_t, t, c_{img}, c_{audio}) - (z_1 - z_0) \right\|_2^2$$

其中 $c_{img}$ 为参考图像条件，$c_{audio}$ 为音频条件，$v_\Theta$ 为DiT预测的速度场，$(z_1 - z_0)$ 为真实速度。该目标驱动模型从噪声逐步恢复视频潜在表示。

### 掩码预测器

掩码预测器是附加在DiT每一Transformer层上的轻量化分支，由跨注意力层与MLP组成。对于第 $l$ 层和第 $i$ 个参考图像，视频令牌 $\mathbf{Q}^v$ 对参考图像的键 $\mathbf{K}_i^r$ 和值 $\mathbf{V}_i^r$ 执行跨注意力：

$$a_i^{(l)} = \operatorname{softmax}\left( \frac{\mathbf{Q}^v \mathbf{K}_i^{r \top}}{\sqrt{d}} \right) \mathbf{V}_i^r$$

注意力输出 $a_i^{(l)}$ 随后通过MLP并经sigmoid激活，产生逐令牌的空间掩码：

$$m_i^{(l)} \gets \operatorname{sigmoid}\left( \mathbf{MLP}(\mathbf{p}_i^{(l)}) \right)$$

该掩码量化了每个视频令牌受第 $i$ 个参考图像影响的程度。训练时使用focal loss监督掩码预测，监督信号来自Grounding-SAM2提取的真实分割掩码。

### 局部音频条件注入

在获得掩码后，框架将wav2vec音频特征仅注入到被掩码标记为属于特定身份的视频令牌中。具体而言，对于第 $i$ 个身份，其音频条件通过掩码 $m_i$ 与静音特征 $\mathbf{p}_i^{\mathrm{mute}}$ 进行混合：

$$\mathbf{h}^v \gets \mathbf{h}^v + m_i \odot \mathbf{p}_i + (1 - m_i) \odot \mathbf{p}_i^{\mathrm{mute}}$$

其中 $\mathbf{h}^v$ 为视频令牌特征，$\odot$ 表示逐元素乘法。该公式确保说话音频仅影响掩码区域内的令牌，而掩码外区域接收静音特征，从而避免不同说话人之间的音频交叉污染。

### 推理时的交错掩码缓存策略

推理时无法获取真实布局，因此框架采用交错掩码预测策略：在第 $k$ 个去噪步预测的掩码被缓存，并作为第 $k+1$ 步音频条件注入的空间先验（见Algorithm 1）。这一设计使得掩码随去噪过程逐步优化，同时每一条件注入步骤都能利用上一步的布局信息，形成自洽的迭代优化循环。消融实验证实，移除掩码缓存会导致多说话人唇同步指标Sync-D从6.921恶化至11.046（Table 12），验证了交错策略对性能的关键作用。

### 开销分析

掩码预测器仅增加约56M参数（相对于7B的DiT主干），每个额外参考图像在每DiT块上仅增加约0.013秒推理时间。完整模型在3个参考图像下的总推理时间为8.9秒（Table 5），表明该模块在几乎不牺牲效率的前提下实现了显著的性能增益。



## 实验与关键发现

### 主要结果

InterActHuman 在音频驱动的多人物动画和多概念视频定制两项核心任务上均取得了最优性能。

**音频驱动多人物动画**：Table 1 的定量对比显示，本方法在多人物测试集上取得了最低的 FVD（22.881），显著优于商业方案 Kling1.6+Lip-sync（33.555）和开源方案 OmniHuman（27.048）。在唇同步指标 Sync-D 上，本方法（6.670）同样优于使用真实固定掩码的 OmniHuman（7.068），表明预测的动态掩码在无真实布局信息的情况下，能够更精确地实现音频-说话人的空间绑定。在单人物测试集上，本方法取得最高的 HKV（59.635），验证了方法在保持视频质量方面的一致性。


![[assets/figures/papers/paper_list_l15_https_openreview_net_forum_id_rJilRU8D3c/figures/005_Table_1.jpg]]
*Table 1: Quantitative comparisons with audio-conditioned full-body animation baselines*

**多概念视频定制**：Table 3 的结果表明，本方法在主体一致性指标上全面领先。CLIP-I 达到 0.744，DINO-I 达到 0.533，分别比最强基线 Phantom* 高出 0.041 和 0.057。面部细节保持方面，Face-Arc（0.598）和 Face-Cur（0.600）同样为最优，说明显式的布局预测机制有效防止了多概念场景下的身份混淆。


![[assets/figures/papers/paper_list_l15_https_openreview_net_forum_id_rJilRU8D3c/figures/007_Table_3.jpg]]
*Table 3: Quantitative comparison of subject consistency, prompt following and visual quality. ⋆ means publicly available version with Wan2.1-1.3B*

**用户偏好研究**：Table 2 展示了更具说服力的人类评估结果。在音频驱动任务上，本方法获得平均分 2.48（OmniHuman 为 1.82），Top-1 选择率达 59.9%；在多概念定制任务上，平均分 4.01（Vidu2.0 为 3.40），Top-1 选择率 49.4%。两项任务均显著领先，且优势在统计上具有高置信度（confidence ≥ 0.98）。


![[assets/figures/papers/paper_list_l15_https_openreview_net_forum_id_rJilRU8D3c/figures/006_Table_2.jpg]]
*Table 2: User preference evaluation. ⋆ means publicly available version with Wan2.1-1.3B*

### 消融实验

消融实验系统性地验证了布局对齐音频注入的核心设计选择（Table 4）。


![[assets/figures/papers/paper_list_l15_https_openreview_net_forum_id_rJilRU8D3c/figures/009_Table_4.jpg]]
*Table 4: Ablation study on audio-driven multi-person animation methods*

**音频注入策略对比**：四种变体的对比揭示了因果链条：
- **全局音频注入**（Global audio）：Sync-D 为 9.482，FVD 为 33.895，表现最差。这说明无条件地将音频特征广播到所有空间位置会导致说话人混淆，尤其在多人物场景中。
- **ID 嵌入**（ID Embedding）：Sync-D 改善至 8.627，但 FVD 升至 42.722。通过身份嵌入来区分音频来源有一定帮助，但缺乏空间约束导致视频质量下降。
- **固定掩码**（Fixed Mask）：Sync-D 进一步改善至 7.068，但 FVD 恶化至 40.239。固定掩码提供了空间先验，但无法适应视频中的动态变化，反而引入了不一致性。
- **预测动态掩码**（Ours）：取得最优 Sync-D（6.670）和最优 FVD（22.881），同时在 IQA（4.757）和 AES（3.467）上也最高。这验证了核心洞察：从含噪视频特征中自适应预测布局，是实现高质量多身份同步动画的关键。

**掩码缓存的作用**：Table 12 专门消融了推理时的掩码缓存策略。移除缓存后，Sync-D 从 6.921 急剧退化至 11.046，证实了交错掩码预测策略（上一步掩码指导当前步音频注入）是解决推理时无真实布局这一“鸡与蛋”困局的必要条件。


![[assets/figures/papers/paper_list_l15_https_openreview_net_forum_id_rJilRU8D3c/figures/016_Table_12.jpg]]
*Table 12: Mask cache significantly improves multi-person lip sync*

**计算开销分析**：Table 5 显示，掩码预测器仅增加约 56M 参数（相对于 7B 的 DiT 主干），每增加一个参考图像仅增加约 0.4 秒推理时间。在 3 个参考图像的配置下，完整推理时间为 8.9 秒，表明方法在性能与效率之间取得了良好平衡。


![[assets/figures/papers/paper_list_l15_https_openreview_net_forum_id_rJilRU8D3c/figures/010_Table_5.jpg]]
*Table 5: Runtime and parameters versus number of reference images*

### 失败模式

尽管方法整体表现优异，仍存在若干已知局限：

1. **严重重叠场景下的掩码预测**：当多个人物高度重叠时，掩码预测可能出现不准确，导致音频分配错误。Figure 5 定性展示了此类失败案例，提示在密集交互场景中需要更强的空间推理能力。

2. **掩码边界精度受限**：掩码预测在 VAE 的低分辨率潜在空间中进行，下采样比可能导致边界不够精确。这一问题在高运动强度场景中更为明显（Table 10 中高运动强度下的掩码 IoU 低于 Table 9 中的低运动强度场景）。

3. **人数扩展的泛化性**：训练数据主要包含 2-3 人的对话场景。Table 13 显示扩展到 4-5 人时性能保持稳定（Sync-D 6.608 vs. 6.670），但尚未针对更大规模人群进行专门优化。


![[assets/figures/papers/paper_list_l15_https_openreview_net_forum_id_rJilRU8D3c/figures/017_Table_13.jpg]]
*Table 13: Stable performance when scaling to 4–5 subjects*

4. **文本先验偏差**：由于基座模型为 T2V 扩散模型，当文本提示与训练数据分布偏差较大时，可能生成不自然的内容。这一局限源于基座模型的先验，而非本方法特有的问题。

### 补充图表

![[assets/figures/papers/paper_list_l15_https_openreview_net_forum_id_rJilRU8D3c/figures/013_Table_6.jpg]]
*Table 6: CelebV-HQ: higher is better for IQA/ASE/Sync-C; lower is better for FID*

![[assets/figures/papers/paper_list_l15_https_openreview_net_forum_id_rJilRU8D3c/figures/014_Table_7.jpg]]
*Table 7: RAVDESS: higher is better for IQA/ASE/Sync-C; lower is better for FID*

![[assets/figures/papers/paper_list_l15_https_openreview_net_forum_id_rJilRU8D3c/figures/015_Table_8.jpg]]
*Table 8: Qualitative capability comparison. ✓: supported; x: not supported*




## 定位与知识库关联

### 1. 问题定位与核心瓶颈

InterActHuman 瞄准的是**多概念人体动画**中一个尚未被充分解决的瓶颈：当多个身份（说话人）同时出现在视频中时，如何将不同的音频信号精确地绑定到对应的空间区域。现有方法普遍采用**全局条件注入**策略——音频特征通过交叉注意力或自适应归一化统一作用于所有视频令牌，导致模型必须隐式学习“谁在说话”的对应关系。这在单说话人场景下尚可工作，但在多说话人对话中频繁出现**音频-身份错误对齐**：A的音频驱动了B的口型，或背景噪声干扰了唇同步。

这一瓶颈的根源在于“鸡与蛋”困局：模型既需要空间布局来分配音频，又需要音频来推断布局。InterActHuman 的因果杠杆是在扩散 Transformer 中引入一个**显式的掩码预测分支**，通过迭代缓存和交错预测策略打破这一循环——模型从含噪视频特征中预测身份布局，再用上一步的布局指导下一步的局部音频注入。

### 2. 与基线方法的关系

#### 2.1 音频驱动人体动画基线

InterActHuman 直接对标的是**OmniHuman**（Lin et al., 2025a），后者代表了当前音频驱动人体动画的最高水平。OmniHuman 采用全局音频条件注入，依赖模型注意力机制隐式学习音频-区域的对应关系。InterActHuman 的核心改进在于将这种隐式学习替换为**显式的掩码预测与局部注入**：仅在掩码预测区域内的令牌注入对应身份的 wav2vec 特征，而非全局均匀注入。

在量化对比中（Table 1），InterActHuman 在多说话人测试集上取得了 **FVD 22.881**，显著优于 OmniHuman 的固定掩码变体（Sync-D 7.068）和商业方案 **Kling1.6 + Lip-sync**（Kuaishou, 2024）的 FVD 33.555。用户偏好研究（Table 2）进一步验证了这一优势：在音频驱动多说话人视频任务上，InterActHuman 的平均得分（2.48）和 Top-1 选择率（59.9%）均显著高于 OmniHuman（1.82, 21.3%）。

其他音频驱动基线包括 **DiffTED**（Hogue et al., 2024）、**DiffGest + Mimiction**（Zhu et al., 2023; Zhang et al., 2024）和 **CyberHost**（Lin et al., 2024），这些方法主要面向单说话人场景，未涉及多身份布局对齐问题，因此在多说话人设定下缺乏直接可比性。

#### 2.2 多概念视频定制基线

在多概念定制维度上，InterActHuman 与 **ConceptMaster**（Huang et al., 2025）、**Video-Alchemist**（Chen et al., 2025a）和 **Phantom**（Liu et al., 2025）形成对比。这些方法侧重于将多个参考概念的外观注入生成视频，但缺乏对**音频条件与概念的空间绑定**机制。Table 3 显示，InterActHuman 在主体一致性指标上全面领先：CLIP-I 达到 0.744（Phantom* 为 0.703），DINO-I 达到 0.533（Phantom* 为 0.476），面部保真度指标 Face-Arc、Face-Cur、Face-Glink 也均取得最优。

商业方案如 **Vidu2.0**（Bao et al., 2024）和 **Pika2.1** 在用户偏好研究中（Table 2）得分分别为 3.40 和 2.78，远低于 InterActHuman 的 4.01，表明通用视频生成模型在多概念定制场景下难以保持身份一致性和音频同步。

#### 2.3 多说话人头部动画基线

**MultiTalk** 是专门面向多说话人头部动画的方法，但其技术路线与 InterActHuman 的全身体动画框架存在本质差异。InterActHuman 通过统一的掩码预测机制同时处理头部和全身动画，避免了任务特定的架构设计。

### 3. 方法谱系中的位置

从方法谱系角度看，InterActHuman 处于以下三条技术路线的交汇点：

- **扩散 Transformer 视频生成**：基于 MMDiT 架构，采用流匹配（Flow Matching）训练目标，继承了 Wan2.1-1.3B 的预训练先验。这使其与 OmniHuman、Phantom 等共享相似的基础架构。
- **显式布局引导的条件注入**：通过跨注意力掩码预测器将布局信息显式化，区别于依赖注意力隐式学习布局的主流方案。这一设计选择使 InterActHuman 在可控性和可解释性上具有优势，但也引入了掩码质量对性能的依赖。
- **迭代推理缓存策略**：在去噪过程中缓存上一步的掩码预测结果，用于指导当前步的条件注入。这种交错策略（interleaved mask-prediction）是解决推理时无真实布局问题的关键创新。

### 4. 适用边界与局限

#### 4.1 已验证的适用场景

- **多说话人对话动画**（2-3人）：训练数据主要覆盖此规模，Table 13 显示扩展到 4-5 人时性能保持稳定，但未针对更大规模优化。
- **全身体动画与面部动画**：统一框架同时处理头部和全身，Table 6（CelebV-HQ）和 Table 7（RAVDESS）验证了在单说话人基准上的竞争力。
- **多概念外观定制**：支持人物、物体、场景的组合生成，包括换装、人-物交互、动漫风格等（Figure 1）。

#### 4.2 已知局限

1. **严重重叠场景下的掩码预测失效**：当多个人物高度重叠时，掩码预测器难以准确区分身份边界，导致音频分配错误（Figure 5 展示了失败案例）。这是显式掩码方法的固有弱点——低分辨率潜在空间（VAE 下采样）加剧了边界模糊问题。

2. **训练数据规模限制**：训练语料主要包含 2-3 人的对话场景（2.6M 视频-掩码-描述三元组），对 4 人以上场景的泛化仅经过初步验证，尚未系统优化。

3. **文本先验偏差**：由于基础模型为 T2V 架构，当文本提示与训练数据分布偏差较大时，可能生成不自然的内容。这是继承自预训练模型的限制，而非方法本身的设计缺陷。

4. **掩码边界精度受限于 VAE**：掩码预测在 VAE 压缩的潜在空间中进行，低分辨率导致边界不够精确。这是当前扩散视频生成方法的共性问题。

5. **非人类中心场景未充分验证**：方法设计围绕人体动画展开，在纯物体交互或无人物场景上的表现尚待评估。

### 5. 开放问题

- **掩码预测的鲁棒性提升**：如何改进掩码预测器以处理高度重叠区域？可能的路径包括引入更高分辨率的特征层、多尺度掩码预测，或结合光流信息增强时序一致性。

- **边界精度的根本性改进**：低 VAE 下采样比是当前扩散模型的架构约束。是否可以通过级联细化（cascaded refinement）或在像素空间进行后处理来补偿掩码边界的不精确？

- **任意数量输入的泛化**：训练数据中仅包含 2-3 个个体，如何使模型泛化到任意数量的输入？这可能需要改进训练数据构造策略或引入数量无关的架构设计。

- **隐式方法的潜在超越**：当前显式掩码方案在可控性上占优，但隐式匹配方案（如更强的注意力机制或可学习的空间绑定）是否可能在未来以更低的计算开销达到同等或更优的性能？

- **跨模态布局绑定**：布局条件机制是否可以扩展到其他模态？例如将文本描述绑定到特定空间区域，实现更精细的文本引导视频生成。



## 原文 PDF

![[paperPDFs/ICLR_2026/InterActHuman_Multi_Concept_Human_Animation_with_Layout_Aligned_Audio_Conditions.pdf]]

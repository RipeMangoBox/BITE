---
title: "VideoPainter: Any-length Video Inpainting and Editing with Plug-and-Play Context Control"
type: paper
paper_level: A
venue: SIGGRAPH
year: 2025
pdf_ref: paperPDFs/SIGGRAPH_2025/VideoPainter_Any_length_Video_Inpainting_and_Editing_with_Plug_and_Play_Context_Control.pdf
project_link: "https://yxbian23.github.io/project/video-painter"
code_link: "https://github.com/Breakthrough/PySceneDetect"
aliases:
- VideoPainter
tags:
- SIGGRAPH_2025
- topic/vision_multimodal_applications
core_operator: 通过双分支架构解耦背景上下文提取与前景生成，利用掩码选择性特征注入指导预训练DiT，并引入目标区域ID重采样实现长视频身份一致性。
primary_logic: 仅需克隆预训练DiT的前两层作为轻量上下文编码器（6%参数量），将掩码选择性背景特征分组注入冻结的DiT骨干，即可高效实现背景保留与文本引导的前景生成；同时，通过将前序片段修复区域的令牌追加到当前KV向量进行重采样，可在不修改骨干的情况下维持任意长度视频的对象身份一致性。
claims:
- 在VPBench标准分割掩码视频修复任务中，VideoPainter在PSNR、SSIM、LPIPS、FVID等全部8项指标上均取得最优结果，PSNR达到23.32，SSIM 0.89，LPIPS 6.85，FVID 0.15，显著超越ProPainter、COCOCO和Cog-Inp。
- 双分支VideoPainter相较单分支微调基线在所有指标上大幅领先（PSNR 23.32 vs 20.54），训练损失曲线证明双分支解耦具有更优的收敛起点与稳定性。
- 用户调研显示，VideoPainter在视频修复的背景保留（74.2%）、文本对齐（82.5%）、视频质量（87.4%）三项指标上均获得压倒性偏好。
- 移除目标区域ID重采样后，长视频修复性能下降明显（PSNR 21.79 vs 22.19），且ID属性随视频长度增加逐渐退化。
---

# VideoPainter: Any-length Video Inpainting and Editing with Plug-and-Play Context Control

> [!tip] 核心洞察
> 仅需克隆预训练DiT的前两层作为轻量上下文编码器（6%参数量），将掩码选择性背景特征分组注入冻结的DiT骨干，即可高效实现背景保留与文本引导的前景生成；同时，通过将前序片段修复区域的令牌追加到当前KV向量进行重采样，可在不修改骨干的情况下维持任意长度视频的对象身份一致性。

| 字段 | 内容 |
|------|------|
| 中文题名 | VideoPainter：支持任意长度视频修复与编辑的即插即用上下文控制 |
| 英文题名 | VideoPainter: Any-length Video Inpainting and Editing with Plug-and-Play Context Control |
| 会议/期刊 | SIGGRAPH 2025 |
| Links | [paper](http://arxiv.org/abs/2503.05639v3) · [Project](https://yxbian23.github.io/project/video-painter) · [Code](https://github.com/Breakthrough/PySceneDetect) |
| Topic | #topic/vision_multimodal_applications |
| Method | VideoPainter |
| Dataset | VPBench Standard Segmentation, VPBench Long Video Segmentation, Davis Random Mask, VPBench Standard Video Editing |

> [!tip] 效果简介
> - VPBench Standard Segmentation 上，PSNR / SSIM / LPIPS / FVID 等8项综合指标 PSNR 23.32, SSIM 0.89, LPIPS 6.85, FVID 0.15 vs 次优结果：Cog-Inp PSNR 22.15, SSIM 0.82, LPIPS 9.56, FVID 0.18 (PSNR +1.17, SSIM +0.07, LPIPS -2.71, FVID -0.03)。
> - VPBench Long Video Segmentation 上，PSNR / SSIM / LPIPS / FVID PSNR 22.19, SSIM 0.85, LPIPS 9.14, FVID 0.17 vs Cog-Inp PSNR 19.78, SSIM 0.73, LPIPS 12.53, FVID 0.21 (PSNR +2.41)。
> - Davis Random Mask 上，PSNR / SSIM / LPIPS / FVID PSNR 25.27, SSIM 0.94, LPIPS 4.29, FVID 0.09 vs ProPainter PSNR 23.99, SSIM 0.92 (PSNR +1.28)。

## 概要

**问题**：现有视频修复方法面临两大瓶颈——单分支生成式架构难以在同一模型中兼顾背景保真度与前景生成质量，且长视频生成时缺乏有效的身份一致性保持机制，导致对象属性随视频长度增加逐渐退化。

**方法**：本文提出VideoPainter，一个双分支即插即用框架。核心思路是将视频修复解耦为背景保留与前景生成两个子任务：仅克隆预训练扩散Transformer（DiT）的前两层作为轻量上下文编码器（参数量仅为骨干的6%），通过掩码选择性特征注入将纯背景令牌的编码特征分组融入冻结的DiT骨干，实现高效的背景控制；同时引入目标区域ID重采样机制，将前序片段修复区域的令牌追加到当前KV向量，在无需修改骨干的前提下维持任意长度视频的对象身份一致性。

**主要结果**：在VPBench标准分割掩码视频修复任务中，VideoPainter在PSNR（23.32）、SSIM（0.89）、LPIPS（6.85）、FVID（0.15）等全部8项指标上取得最优，显著超越ProPainter、COCOCO和Cog-Inp等基线。长视频修复PSNR达22.19，领先次优方法2.41 dB。用户调研中，VideoPainter在背景保留（74.2%）、文本对齐（82.5%）和视频质量（87.4%）三项指标上均获得压倒性偏好。消融实验证实双分支解耦、选择性令牌集成和ID重采样对性能至关重要。

**定位**：VideoPainter是首个支持即插即用背景控制的视频修复双分支框架，与任何预训练DiT骨干兼容，在生成质量与身份一致性上树立了新基准。

## 核心方法与创新机理

### 核心瓶颈：单分支架构的背景-前景耦合困境

现有生成式视频修复方法普遍采用单分支架构——将待修复视频、噪声潜变量与掩码直接拼接后输入扩散Transformer（DiT）进行统一处理。这种设计面临一个根本性矛盾：**背景区域的像素级保真度要求模型精确复制原始内容，而前景生成区域则需要模型基于文本提示进行创造性合成**。单分支网络被迫在同一参数空间中同时优化这两个相互冲突的目标，导致背景保留与前景生成质量难以兼得。此外，在长视频生成中，缺乏显式的身份一致性保持机制使得前序片段的修复对象属性（纹理、颜色、形状）在后续片段中逐渐退化。

### 核心洞察：双分支解耦 + 掩码选择性注入

VideoPainter的核心创新在于通过**双分支架构实现背景保留与前景生成的显式解耦**，并以极低的参数代价实现即插即用的上下文控制。其关键洞察是：预训练DiT已经具备强大的生成先验，无需对其进行微调；仅需克隆其前两层作为轻量上下文编码器（仅占骨干参数的6%），专门负责提取背景上下文特征，再通过掩码选择性注入机制将背景信息精确地引导至冻结的DiT骨干，即可高效完成背景保留；而DiT骨干自身则专注于文本引导的前景生成。

### 三个关键的结构性改变（Changed Slots）

**1. 架构设计：从单分支DiT到双分支解耦架构**

| 维度 | 基线方案（Cog-Inp等） | VideoPainter方案 |
|------|----------------------|------------------|
| 架构 | 单分支DiT，在输入通道拼接待修复视频+噪声+掩码 | 双分支：轻量上下文编码器（克隆DiT前两层，6%参数量）+ 冻结的预训练DiT骨干 |
| 背景处理 | 与前景统一处理，无专用背景保留机制 | 上下文编码器专门提取背景特征，DiT骨干专注于前景生成 |
| 训练策略 | 全参数微调或部分微调骨干 | 仅训练上下文编码器，骨干完全冻结 |

消融实验（Table 7）证实，双分支架构相较单分支微调基线在PSNR上提升达2.78（23.32 vs 20.54），训练损失曲线（Fig. 8）显示双分支方案具有更优的收敛起点与稳定性，验证了解耦设计的必要性。

![[assets/figures/papers/paper_list_l11_http_arxiv_org_abs_2503_05639v3/figures/012_Table_7.jpg]]
*Table 7: Ablation Studies on VPBench. Single-Branch: We add input channels to adapt masked video and finetune the backbone. Layer Configuration (VideoPainter (*)): We vary the context encoder depth from one to four layers. w/o Selective Token Integration (w/o Select):: We bypass the token pre-selection step and integrate all context encoder tokens into DiT. T2V Backbone (VideoPainter (T2V)): We replace the backbone from image-to-video DiTs to text-to-video DiTs. w/o target region ID resampling (w/o Resample): We ablate on the target region ID resampling. (L) denotes evaluation on the long video subset. Red stands for the best result*

![[assets/figures/papers/paper_list_l11_http_arxiv_org_abs_2503_05639v3/figures/013_Figure_8.jpg]]
*Figure 8: Training loss curve of ablation of single branch fine-tuning and default dual branch VideoPainter. The training loss curves demonstrate that our dual-branch VideoPainter achieves superior convergence speed, stability, and final performance compared to single-branch fine-tuning, despite having significantly fewer trainable parameters*

**2. 特征注入方式：从无专用注入到分组式令牌选择性注入**

上下文编码器的特征并非简单地全部注入DiT，而是采用两层分组策略：
- **分组注入**：上下文编码器的第1层输出注入DiT的前半部分层，第2层输出注入DiT的后半部分层，实现分层级的背景控制。
- **令牌选择性过滤**：仅将掩码区域外的**纯背景令牌**的编码特征加回DiT骨干，前景区域的令牌被预先滤除，避免前景/背景信息混淆。

特征注入公式为：

$$\epsilon_{\theta}(z_{t}, t, C)_{i} = \epsilon_{\theta}(z_{t}, t, C)_{i} + \mathcal{Z}\left(\epsilon_{\theta}^{VideoPainter}\left([z_{t}, z_{0}^{masked}, m^{resized}], t\right)_{i / {\frac{n}{2}}}\right)$$

其中$\epsilon_{\theta}$为冻结的DiT骨干，$\epsilon_{\theta}^{VideoPainter}$为上下文编码器，$z_t$为噪声潜变量，$z_0^{masked}$为掩码视频潜变量，$m^{resized}$为下采样掩码，$\mathcal{Z}$为零填充操作（仅背景令牌位置保留编码值，其余位置置零），$i$为DiT层索引，$n$为总层数。该公式表明上下文编码器的第$i/\frac{n}{2}$层输出经令牌选择性过滤后，逐元素加至DiT骨干第$i$层的对应位置。

消融实验显示，移除选择性令牌集成后PSNR骤降至20.94、SSIM降至0.74（Table 7，w/o Select），证实掩码过滤对防止骨干信息混淆至关重要。

**3. 长视频身份一致性：从无显式机制到目标区域ID重采样**

传统方法（如AVID）依赖重叠片段生成和特征平滑来维持片段间一致性，缺乏对修复对象身份的显式约束。VideoPainter引入**目标区域ID重采样**机制：
- **训练阶段**：在冻结的DiT骨干中插入可训练的LoRA适配器（ID Resample Adapter），将当前修复区域的令牌拼接到KV（Key-Value）向量中，使模型学会从上下文中重采样身份信息。
- **推理阶段**：将前序片段修复区域的令牌追加到当前片段的KV向量中，形成扩展的$[K_i^v, K_i^{id}]$和$[V_i^v, V_i^{id}]$，使当前片段在生成时能够显式地重采样前一帧的ID属性。

消融实验（Table 9）表明，移除ID重采样后长视频修复PSNR从22.19降至21.79，且定性结果（Fig. 9）显示修复区域的纹理和颜色随视频长度增加而逐渐衰减，验证了该机制对维持任意长度视频身份一致性的关键作用。

![[assets/figures/papers/paper_list_l11_http_arxiv_org_abs_2503_05639v3/figures/017_Table_9.jpg]]
*Table 9: Ablation Studies on VPBench: w/o target region ID resampling (w/o Resample): We ablate on the target region ID resampling. (L) denotes evaluation on the long video subset. Red stands for the best result*

### 流水线模块总览

VideoPainter的整体流水线由以下模块协同构成：
- **Context Encoder**：轻量双层次编码器，接收噪声潜变量、掩码视频潜变量和下采样掩码的拼接输入，提取背景上下文特征。
- **Pre-trained DiT Backbone**：冻结的预训练扩散Transformer（默认CogVideo-5B-I2V），负责前景生成与视频质量。
- **Group-wise Feature Injection**：将上下文编码器特征按层分组注入骨干前半和后半部分。
- **Mask-Selective Token Filtering**：根据掩码信息预过滤，仅将背景令牌特征融合到骨干。
- **ID Resample Adapter**：可训练的LoRA适配器，插入冻结DiT中，支持KV向量拼接以实现目标区域ID重采样。

![[assets/figures/papers/paper_list_l11_http_arxiv_org_abs_2503_05639v3/figures/002_Figure_2.jpg]]
*Figure 2: Framework Comparison. Non-generative approaches, limited to pixel propagation from backgrounds, fail to inpaint fully segmentation-masked objects. Generative methods adapt single-branch image inpainting models to video by adding temporal attention, struggling to maintain background fidelity and generate foreground contents in one model. In contrast, VideoPainter implements a dual-branch architecture that leverages an efficient context encoder with any pre-trained DiT, decoupling video inpainting to background preservation and foreground generation, and enabling plug-and-play video inpainting control*

## 实验与关键发现

### 核心定量结果

VideoPainter 在视频修复和编辑两个任务上均取得全面最优。在 VPBench 标准分割掩码视频修复基准上，VideoPainter 的 PSNR 达到 **23.32**，SSIM **0.89**，LPIPS **6.85**，FVID **0.15**，在所有 8 项指标上均超越 ProPainter、COCOCO 和 Cog-Inp 等基线（Table 2）。其中相较最强生成式基线 Cog-Inp（PSNR 22.15），PSNR 提升 **+1.17**，LPIPS 降低 **2.71**，表明双分支架构在掩码区域保真度上具有显著优势。

在长视频修复子集上，VideoPainter 的优势进一步扩大：PSNR 达 **22.19**，相较 Cog-Inp 的 19.78 提升 **+2.41**（Table 2），验证了 ID 重采样机制对长序列一致性的关键作用。在 Davis 随机掩码基准上，VideoPainter 同样取得最优（PSNR 25.27 vs ProPainter 23.99），证明方法对不同掩码类型具有良好的泛化性。

视频编辑任务中，VideoPainter 在 VPBench 标准视频编辑基准上 PSNR 达 **22.63**，远超 ReVideo 的 15.52（**+7.11**）；长视频编辑子集上 PSNR 为 22.60（+7.10），显示双分支架构对编辑场景同样有效（Table 3）。

![[assets/figures/papers/paper_list_l11_http_arxiv_org_abs_2503_05639v3/figures/009_Table_3.jpg]]
*Table 3: Quantitative comparisons among VideoPainter and other video editing models in VPBench (Standard and Long Video): UniEdit [Bai et al. 2024], DitCtrl [Cai et al. 2024], and ReVideo [Mou et al. 2024]. Metrics include masked region preservation, text alignment, and video quality. Red stands for the best, Blue stands for the second best*

### 用户偏好验证

用户调研结果（Table 4/Table 6）提供了感知层面的强证据：在视频修复任务中，VideoPainter 在背景保留（**74.2%**）、文本对齐（**82.5%**）和视频质量（**87.4%**）三项指标上均获得压倒性偏好；视频编辑任务中相应偏好率分别为 78.4%、76.1% 和 81.7%。这一定性优势与定量指标高度一致，说明双分支解耦设计在主观感知上同样有效。

![[assets/figures/papers/paper_list_l11_http_arxiv_org_abs_2503_05639v3/figures/010_Table_4.jpg]]
*Table 4: User Study: User preference ratios comparing VideoPainter with video inpainting and editing baselines. For each sample, participants selected only one model that produced the best results for each criterion. We evaluate performance using the average proportion of being selected as the best response. For video inpainting, we compared VideoPainter against ProPainter [Zhou et al. 2023], COCOCO [Zi et al. 2024], and Cog-Inp [Yang et al. 2024]. For video editing, we compared VideoPainter against UniEdit [Bai et al. 2024], DitCtrl [Cai et al. 2024], and ReVideo [Mou et al. 2024]. Detailed results are in the appendix*

![[assets/figures/papers/paper_list_l11_http_arxiv_org_abs_2503_05639v3/figures/014_Table_6.jpg]]
*Table 6: User study evaluation comparing VideoPainter against stateof-the-art video inpainting and editing models. We conducted comprehensive comparisons on the VPBench, randomly sampling 50 examples from each of the inpainting and editing subsets. Human evaluators assessed the models’ outputs based on three criteria: background preservation, text alignment, and overall video quality. For each sample, participants selected only one model that produced the best results for each criterion. We evaluate performance using the proportion of model-generated outputs selected as the optimal response across all samples. For video inpainting, we compared against ProPainter [Zhou et al. 2023], COCOCO [Zi et al....*

### 关键消融发现

**双分支 vs 单分支**：将 VideoPainter 的双分支架构替换为单分支微调后，PSNR 从 23.32 骤降至 **20.54**（Table 7）。训练损失曲线（Fig. 8）进一步揭示，双分支架构不仅最终性能更优，且收敛速度更快、训练更稳定。这直接验证了背景保留与前景生成的解耦是性能提升的核心因果机制。

**上下文编码器深度**：编码器层数从默认的 2 层变为 1 层或 4 层时，性能均出现下降（Table 7），表明 2 层结构在效率与表征能力之间达到了最优平衡。

**掩码选择性令牌注入**：移除令牌预过滤步骤（w/o Select）后，PSNR 降至 **20.94**，SSIM 降至 **0.74**（Table 7）。这表明若不区分前景/背景令牌、将所有上下文编码器输出注入 DiT 骨干，会造成严重的信息混淆，破坏背景保真度。

**ID 重采样**：去除目标区域 ID 重采样后，长视频修复 PSNR 从 22.19 降至 **21.79**（Table 9），且定性结果（Fig. 9）显示修复区域的纹理和颜色随视频长度增加逐渐退化。这证实了 ID 重采样是维持任意长度视频身份一致性的必要条件。

### 适用边界与失效模式

VideoPainter 的性能受限于以下边界条件：
- **基础模型能力**：生成质量受限于预训练 DiT（默认 CogVideo-5B-I2V），对复杂物理运动和精细结构建模可能存在不足。
- **掩码质量敏感性**：对随机矩形掩码的修复性能相较分割掩码下降约 **13%**（Table 8），主要源于矩形边缘与自然分割边界的几何差异引入边缘伪影。但对不同膨胀/腐蚀核大小的分割掩码表现出良好鲁棒性。
- **文本描述依赖**：低质量或与视频内容不匹配的文本描述会导致生成结果退化，这是文本引导生成方法的共性局限。

![[assets/figures/papers/paper_list_l11_http_arxiv_org_abs_2503_05639v3/figures/015_Table_8.jpg]]
*Table 8: Ablation Studies on VPBench: Kernel (*): We randomly sample dilation and erosion with varying kernel sizes ∈ (8, 16, 32) for the segmentation masks. Kernel (Square): We randomly sample square masks with varying sizes ∈ [8, 32] and random locations. This reflects VideoPainter’s robustness to different mask qualities. Red stands for the best result*

## 定位与知识库关联

VideoPainter 的核心定位在于将视频修复与编辑任务从传统的“单分支统一建模”范式，迁移至“双分支解耦控制”范式。其本质差异在于，现有方法（无论是非生成式的像素传播，还是生成式的单分支微调）均试图在单一模型中同时处理背景保留与前景生成，导致两个目标相互掣肘。VideoPainter 通过引入一个仅占骨干参数量 6% 的轻量上下文编码器，将背景上下文提取任务从冻结的预训练 DiT 骨干中彻底剥离，从而将骨干的全部容量释放给前景生成与文本对齐。

**与现有基线的本质差异**

*   **相较非生成式方法（如 ProPainter, Zhou et al., CVPR 2023）**：非生成式方法的核心瓶颈在于其仅能通过光流或注意力机制从相邻帧的背景区域传播像素信息，因此当待修复区域完全被分割掩码覆盖时，模型缺乏生成新内容的能力。VideoPainter 依托预训练 DiT 的生成先验，可直接合成掩码区域内的任意新对象，突破了像素传播的物理限制。

*   **相较生成式单分支方法（如 COCOCO, Zi et al., 2024；Cog-Inp）**：这类方法通常在输入通道维度拼接掩码视频与噪声潜变量，并整体微调骨干网络。这迫使同一组参数同时学习“保持背景不变”和“生成新前景”两个相互冲突的目标，导致背景保真度与前景生成质量难以兼得。VideoPainter 的双分支解耦设计（Table 7, Fig. 8）从根本上消除了这一冲突：上下文编码器专门负责提取背景特征，并通过掩码选择性注入机制仅将纯背景令牌信息传递给冻结的骨干，避免了前景/背景令牌的信息混淆。训练损失曲线（Fig. 8）直观地证明了双分支架构在收敛起点、速度和稳定性上均显著优于单分支微调。

*   **相较视频编辑方法（如 UniEdit, Bai et al., 2024；ReVideo, Mou et al., 2024）**：多数编辑方法依赖 DDIM 反演来获取初始噪声，其编辑能力受限于反演精度。VideoPainter 则直接利用掩码视频潜变量作为上下文编码器的输入，无需反演过程，从而在编辑任务中实现了显著更高的重建保真度（VPBench 标准编辑 PSNR 22.63 vs. ReVideo 15.52）。

**知识库挂载点**

VideoPainter 在方法论上连接了以下关键知识节点：

1.  **预训练 DiT 的即插即用控制**：VideoPainter 提供了一种通用的、非侵入式的控制范式。其核心洞察在于，仅需克隆预训练 DiT 的前两层作为上下文编码器，并通过分组式特征注入（前半层输出注入 DiT 前半部分，后半层输出注入 DiT 后半部分），即可在不修改骨干权重的情况下实现对背景的密集控制。这一范式可被视作一种针对 DiT 架构的轻量级适配器（Adapter），为未来将其他预训练 DiT（如 Sora、NVIDIA Cosmos）快速适配至视频修复、编辑乃至更广泛的密集预测任务提供了技术路径。

2.  **长视频生成中的身份一致性**：VideoPainter 提出的目标区域 ID 重采样机制，通过在推理时将前序片段的修复区域令牌追加到当前片段的 KV 向量中进行重采样，实现了一种显式的、可训练的 ID 保持方案。这与 AVID 等依赖重叠片段特征平滑的隐式方法形成对比，为长视频生成中的漂移问题提供了一个更直接的解决方案。该机制以 LoRA 适配器的形式实现，同样保持了即插即用的特性。

**适用边界与局限性**

*   **生成质量上限受限于基础模型**：VideoPainter 的生成能力完全继承自其冻结的预训练 DiT 骨干（默认 CogVideo-5B-I2V）。因此，对于基础模型本身难以处理的复杂物理交互、精细运动建模或罕见概念，VideoPainter 无法提供额外的增益。
*   **文本描述依赖性**：模型的文本对齐能力依赖于输入的视频描述或编辑指令的质量。当文本描述与视频内容不匹配或过于模糊时，生成结果的质量会显著下降。
*   **掩码质量鲁棒性**：尽管 VideoPainter 对分割掩码的膨胀/腐蚀操作具有一定的鲁棒性，但在面对随机矩形掩码时性能下降约 13%（Table 8）。这主要是因为矩形掩码的硬边缘与自然分割掩码的几何特征差异，可能导致上下文编码器提取的背景特征在边界处引入伪影。

**后续工作启发**

1.  **更强基础模型的即插即用适配**：本文展示了在 CogVideo-5B-I2V 上的有效性，并初步验证了在 T2V 骨干上的可迁移性（Table 7）。后续工作可探索将该双分支控制框架应用于更强大的视频生成基础模型（如 Sora 等），以直接提升修复与编辑的生成质量上限。
2.  **上下文编码器的能力扩展**：当前的上下文编码器仅接收单帧掩码潜变量。未来可探索将其扩展为接收多帧输入或引入额外的控制信号（如深度图、边缘图），以进一步增强对复杂场景的背景控制精度。
3.  **ID 重采样机制的泛化**：当前的 ID 重采样聚焦于修复区域本身。后续工作可研究将该机制扩展至多对象交互、对象遮挡与重现等更复杂的长期一致性场景，探索更通用的时空身份保持框架。

## 原文 PDF

![[paperPDFs/SIGGRAPH_2025/VideoPainter_Any_length_Video_Inpainting_and_Editing_with_Plug_and_Play_Context_Control.pdf]]
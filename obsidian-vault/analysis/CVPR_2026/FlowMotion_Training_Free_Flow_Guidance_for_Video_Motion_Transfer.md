---
title: "FlowMotion: Training-Free Flow Guidance for Video Motion Transfer"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/FlowMotion_Training_Free_Flow_Guidance_for_Video_Motion_Transfer.pdf
project_link: null
code_link: null
aliases:
- FlowMotion
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/representation_self_supervised_transfer
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 本文的关键增效环节是：直接利用基于流的T2V模型预测输出的潜在预测（latent predictions）作为运动表示，无需访问内部层或进行反演；通过流引导损失对齐源视频与目标视频的潜在预测及其帧间差异来迁移运动；并引入速度正则化策略稳定迭代优化过程，从而完全消除对内部层梯度传播的依赖。
primary_logic: 核心洞察在于：基于流的T2V模型的早期潜在预测（通过从噪声潜在和预测速度的线性外推获得）天然编码了丰富的时空动态信息，这些信息从粗粒度轨迹逐步演化为细粒度动作，且可在不依赖反演和内部特征的情况下高效提取，为训练无关的运动迁移提供了简洁而高效的引导信号。
claims:
- 基于输出潜在预测的流引导将GPU显存需求从内部特征方法的93.1G及OOM（超出显存）降至19.3G，几乎接近纯推理开销（17.7G），实现极低资源消耗。
- 在50段视频的测试集上，FlowMotion在运动保真度（0.850）和时间一致性（0.986）两个指标上全面超越所有训练无关及训练方法，并在用户研究中获得最高综合评分（4.446），验证了其在运动迁移质量上的优势。
- 消融实验证明：去除差异对齐（DA）后运动保真度从0.850降至0.842，视觉出现伪影；去除速度正则化（VR）后保真度骤降至0.809，时间一致性从0.986降至0.968，画面严重退化，证实了这两个模块各自不可或缺的作用。
- 流引导完全基于模型输出（速度预测）计算，梯度回传仅涉及潜在变量自身，消除对U-Net或DiT内部结构的依赖，使方法可无缝适配不同骨干网络（如Wan2.1‑1.3B与Wan2.2‑5B），展示了强泛化能力。
---

# FlowMotion: Training-Free Flow Guidance for Video Motion Transfer

> [!tip] 核心洞察
> 核心洞察在于：基于流的T2V模型的早期潜在预测（通过从噪声潜在和预测速度的线性外推获得）天然编码了丰富的时空动态信息，这些信息从粗粒度轨迹逐步演化为细粒度动作，且可在不依赖反演和内部特征的情况下高效提取，为训练无关的运动迁移提供了简洁而高效的引导信号。

| 字段 | 内容 |
|------|------|
| 中文题名 | FlowMotion：无需训练的流引导视频运动迁移方法 |
| 英文题名 | FlowMotion: Training-Free Flow Guidance for Video Motion Transfer |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Wang_FlowMotion_Training-Free_Flow_Guidance_for_Video_Motion_Transfer_CVPR_2026_paper.html) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/representation_self_supervised_transfer #topic/vision_multimodal_applications/image_and_video_generation |
| Method | FlowMotion |
| Dataset |  |

> [!tip] 效果简介
> - 基于输出潜在预测的流引导将GPU显存需求从内部特征方法的93.1G及OOM（超出显存）降至19.3G，几乎接近纯推理开销（17.7G），实现极低资源消耗。
> - 在50段视频的测试集上，FlowMotion在运动保真度（0.850）和时间一致性（0.986）两个指标上全面超越所有训练无关及训练方法，并在用户研究中获得最高综合评分（4.446），验证了其在运动迁移质量上的优势。
> - 消融实验证明：去除差异对齐（DA）后运动保真度从0.850降至0.842，视觉出现伪影；去除速度正则化（VR）后保真度骤降至0.809，时间一致性从0.986降至0.968，画面严重退化，证实了这两个模块各自不可或缺的作用。

## 概要

**问题瓶颈**：现有训练无关的视频运动迁移方法依赖从预训练文本生成视频（T2V）模型的中间层（如时间注意力图或扩散特征）提取运动表示，导致梯度必须反向传播穿过深层模型参数，带来极高的GPU显存开销（典型方法超过93 GB甚至超出显存），且与特定骨干架构（U-Net或DiT）紧耦合，灵活性和泛化能力受限。

**核心洞察**：基于流的T2V模型在早期去噪步骤中，由噪声潜在和预测速度经线性外推得到的潜在预测（latent predictions）天然编码了从粗粒度轨迹到细粒度动作的丰富时空动态信息，且这些信息无需访问模型内部层或进行反演即可高效提取，为训练无关的运动迁移提供了简洁而直接的引导信号。

**关键增效环节**：FlowMotion直接利用模型输出的潜在预测作为运动表示，通过流引导损失（结合潜在对齐与帧间差异对齐）将源视频的运动模式迁移至目标生成视频，并引入速度正则化策略沿累积流方向稳定迭代优化过程，从而完全消除对内部层梯度传播的依赖，使显存占用降至接近纯推理水平（19.3 GB vs 17.7 GB）。

**方法定位**：FlowMotion属于训练无关（training-free）的视频运动迁移框架，与需微调参数的训练方法（如**MotionDirector** Zhao et al., ECCV 2024；**MotionInversion** Wang et al., SIGGRAPH 2025）以及依赖中间特征的训练无关方法（如**MotionClone** Ling et al., arXiv 2024；**MOFT** Xiao et al., NeurIPS 2024；**SMM** Yatim et al., CVPR 2024；**DiTFlow** Pondaven et al., CVPR 2025）形成对比。其核心差异在于运动引导信号直接取自模型输出端，而非内部层或可训练参数。

**主要实证结果**：在覆盖多种运动类型的50段视频测试集上，FlowMotion的运动保真度（0.850）和时间一致性（0.986）全面超越所有对比方法，用户研究综合评分最高（4.446）。消融实验证实，差异对齐和速度正则化各自对运动迁移质量有不可或缺的贡献——去除任一组分均导致保真度和一致性显著下降并引入视觉伪影。该方法可无缝适配不同骨干网络（如Wan2.1‑1.3B与Wan2.2‑5B），展现出强泛化能力。



### 视频运动迁移的任务定义与挑战

视频运动迁移旨在将一段源视频中的运动模式（如物体轨迹、相机运动、复杂动作）迁移到基于文本提示生成的目标视频中，同时保持目标视频的语义内容与文本描述一致。该任务的核心挑战在于：如何在无需针对每个源视频重新训练模型的前提下，准确提取并迁移运动信息，同时维持生成视频的时间一致性和视觉质量。

### 现有方法的两个技术范式及其瓶颈

当前视频运动迁移方法主要分为两类：**训练方法**与**训练无关方法**。

**训练方法**（如 **MotionDirector** (Zhao et al., ECCV 2024)、**MotionInversion** (Wang et al., SIGGRAPH 2025)、**DeT** (Shi et al., arXiv 2025) 以及基于 **LoRA** (Hu et al., ICLR 2022) 的微调策略）通过对每个源视频进行额外训练来学习运动模式。这类方法虽然能取得较好的运动保真度，但训练开销大、时间成本高，难以满足快速迁移的实际需求。

**训练无关方法**（如 **MotionClone** (Ling et al., arXiv 2024)、**MOFT** (Xiao et al., NeurIPS 2024)、**SMM** (Yatim et al., CVPR 2024)、**DiTFlow** (Pondaven et al., CVPR 2025)）则试图绕过训练，直接从预训练的文生视频（T2V）模型中提取运动表示。然而，这些方法存在一个**根本性瓶颈**：它们的运动表示依赖于从模型中间层提取的特征——例如时间注意力图、扩散特征或交叉帧注意力流。这一设计导致两个严重后果：

1. **极高的资源开销**：损失函数的梯度必须反向传播穿过整个深层模型（U-Net 或 DiT）的内部参数，导致 GPU 显存占用极高。典型方法的内存需求超过 93 GB 甚至直接超出显存（OOM），使得实际部署极为困难。
2. **架构紧耦合**：由于运动提取与特定的内部层结构绑定，方法难以在不同骨干网络（如 U-Net 与 DiT）之间迁移，泛化能力受限。

### 本文的核心动机与洞察

FlowMotion 的核心动机在于**彻底消除对模型内部层梯度传播的依赖**。作者观察到：基于流匹配（flow matching）的 T2V 模型在生成过程中，其**输出预测——即潜在预测（latent predictions）**——天然编码了丰富的时空动态信息。具体而言，通过从当前噪声潜在和预测速度进行一步线性外推得到的干净潜在估计（$\hat{z}_0(t) = z_t - t v_t$），在去噪的早期步骤中便已呈现出从粗粒度轨迹到细粒度动作的逐步演化过程（如 Figure 3 所示）。

这一洞察揭示了一条全新的技术路径：**直接利用模型输出端的潜在预测作为运动表示**，而无需访问任何内部层或进行迭代反演。由此，FlowMotion 将运动迁移重新定义为一个基于输出的引导优化问题——通过流引导损失（flow guidance loss）对齐源视频与目标视频的潜在预测及其帧间差异，并辅以速度正则化（velocity regularization）稳定迭代过程。该设计使得梯度仅需传播至输入潜在变量自身，内存开销接近纯推理水平，同时天然解除了对特定模型架构的依赖。



## 核心方法与创新机理

FlowMotion 的核心创新在于**将运动迁移的引导信号从模型内部层彻底外移至预测输出层**，从而突破了现有训练无关方法在资源消耗、架构耦合与优化稳定性上的三重瓶颈。以下从三个关键设计槽位展开。

### 运动引导信号：从内部特征到潜在预测

现有训练无关方法普遍依赖从预训练 T2V 模型中间层提取的运动表示——**MotionClone**（Ling et al., arXiv 2024）使用时间注意力图，**MOFT**（Xiao et al., NeurIPS 2024）利用扩散特征，**DiTFlow**（Pondaven et al., CVPR 2025）则基于交叉帧注意力流。这些内部特征虽编码了运动信息，却迫使梯度反向传播穿过深层网络参数，造成极高的计算开销与架构依赖。

FlowMotion 的关键洞察在于：**基于流的 T2V 模型在早期去噪步骤中，其输出的潜在预测（latent predictions）天然编码了丰富的时空动态信息**。具体而言，在流匹配框架下，干净潜在可通过一步线性外推直接估计：

$$\hat{z}_0(t) = z_t - t v_t$$

其中 $v_t$ 是模型预测的速度。如 Figure 3 所示，这些潜在预测在生成早期即从粗粒度轨迹逐步演化为细粒度动作，构成了高质量的运动表示。FlowMotion 以空提示（empty prompt）运行源视频，提取其潜在预测 $\hat{z}_0^{src}(t)$ 作为运动表示，完全绕过了对内部层特征的依赖。

### 梯度传播路径：从贯穿模型到仅触及潜在变量

传统内部特征引导方法需要将损失梯度从中间层反向传播至整个模型，导致显存需求急剧膨胀。如表 Table 4 所示，基于中间特征的方法在 Wan2.1‑1.3B 骨干上需 93.1G 显存甚至超出显存上限（OOM），而 FlowMotion 的流引导仅需 19.3G，几乎接近纯推理开销（17.7G）。这 1.6G 的增量仅来源于对输入潜在变量 $z_t$ 的梯度更新，梯度传播路径被压缩至模型外部，从根本上消除了对 U‑Net 或 DiT 内部结构的依赖。

这一设计还带来了天然的**骨干网络泛化能力**：如 Figure 6 所示，FlowMotion 可无缝适配 Wan2.1‑1.3B 与 Wan2.2‑5B 两种不同规模的骨干，而无需任何架构适配，验证了其与模型内部结构的解耦特性。

### 优化正则化：速度正则化稳定迭代更新

基于潜在预测的优化过程并非天然稳定。FlowMotion 引入**速度正则化（Velocity Regularization）** 来抑制迭代中的突变和过拟合。其核心机制为：将当前速度 $v_t$ 分解为沿累积流方向 $v_t^{avg}$ 的投影分量 $v_t^{proj}$ 与正交分量 $v_t^{orth}$，并通过衰减正交分量来约束更新方向：

$$v_t^{reg} = v_t^{proj} + \gamma \cdot v_t^{orth}$$

其中 $v_t^{avg} = \frac{z_t - z_1}{t - 1}$ 代表从初始噪声到当前潜在的平均流方向，作为正则化的参考基准。该策略在保持运动迁移方向的同时抑制了高频波动，使优化过程平滑收敛。

消融实验（Table 3）严格验证了上述三个设计的各自贡献：去除差异对齐（w/o DA）后运动保真度从 0.850 降至 0.842 并引入视觉伪影；去除速度正则化（w/o VR）后保真度骤降至 0.809、时间一致性从 0.986 降至 0.968，画面严重退化。这证实了流引导的两项损失与速度正则化各自不可替代的作用。



FlowMotion 的整体 pipeline 围绕“将源视频的运动模式迁移至目标文本提示生成的视频”这一目标，构建了一条**无需训练、无需反演、不依赖模型内部层**的引导式生成流程。其核心设计在于：将运动表示从传统的中间层特征（时间注意力图、扩散特征等）转移至基于流的 T2V 模型**直接输出的潜在预测**上，从而彻底切断梯度向模型内部参数传播的路径。

### 流程总览

如 Figure 4 所示，整个框架由五个串行模块构成，输入为一段源视频和一个目标文本提示，输出为包含源视频运动模式的目标生成视频：

![[assets/figures/papers/paper_list_l3_https_openaccess_thecvf_com_content_CVPR2026_html_Wang_FlowMotion_Traini/figures/004_Figure_4.jpg]]
*Figure 4: The overview of FlowMotion. (a) Training-free video motion transfer with flow guidance and velocity regularization. (b) Two objective of flow guidance. (c) The velocity regularization process*

1. **源视频编码与前向加噪**  
   源视频首先通过 VAE 编码器得到干净潜在序列 $z_0^{src}$，随后利用流匹配模型的线性插值特性，**直接通过公式 $z_t^{src} = (1-t)z_0^{src} + t z_1^{src}$ 获得任意时间步 $t$ 的噪声潜在**，其中 $z_1^{src} \sim \mathcal{N}(0,1)$ 为随机噪声。这一设计完全规避了现有方法中必需的 DDIM 反演或流反演步骤，消除了反演带来的计算开销和误差累积。

2. **潜在预测提取（运动表示构建）**  
   将噪声潜在 $z_t^{src}$ 送入预训练的流匹配 T2V 模型，使用**空提示**（null prompt）预测速度场 $v_t^{src}$，进而通过一步外推得到源视频的潜在预测：
   
$$
\hat{z}_0^{src}(t) = z_t^{src} - t \cdot v_t^{src}
$$

   这一潜在预测 $\hat{z}_0^{src}(t)$ 即为源视频的运动表示。如 Figure 3 所示，在早期去噪步骤（$t$ 接近 1）中，潜在预测已编码了从粗粒度运动轨迹到细粒度动作的丰富时空动态信息，且提取过程完全不涉及模型内部层访问。

3. **流引导（运动迁移核心）**  
   对于目标视频的生成，从随机噪声 $z_1 \sim \mathcal{N}(0,1)$ 出发，在每个去噪步骤中同样计算其潜在预测 $\hat{z}_0(t) = z_t - t \cdot v_t$。流引导损失 $\mathcal{L}_{FG}$ 由两项加权组成：
   
$$
\mathcal{L}_{FG} = \alpha \| \hat{z}_0^{src}(t) - \hat{z}_0(t) \|_2^2 + \beta \| \triangle(\hat{z}_0^{src}(t)) - \triangle(\hat{z}_0(t)) \|_2^2
$$

   - **潜在对齐（Latent Alignment，LA）**：直接约束目标潜在预测与源潜在预测在每一帧上的一致性，传递绝对空间位置上的运动信息。
   - **差异对齐（Difference Alignment，DA）**：约束相邻帧之间潜在预测的差值一致，确保帧间动态变化模式（即运动的变化量）被完整保留。

   梯度仅从 $\mathcal{L}_{FG}$ 回传至目标潜在变量 $z_t$ 本身，**不经过模型内部参数**，这是 FlowMotion 实现极低内存开销和架构无关性的关键。

4. **速度正则化（优化稳定）**  
   在基于流引导损失优化 $z_t$ 的过程中，直接使用模型预测的速度 $v_t$ 进行更新可能导致突变和过拟合。FlowMotion 引入速度正则化策略：首先计算从初始噪声 $z_1$ 到当前潜在 $z_t$ 的平均流方向 $v_t^{avg}$ 作为累积运动趋势的参考，然后将当前速度 $v_t$ 分解为沿 $v_t^{avg}$ 方向的投影分量 $v_t^{proj}$ 和正交分量 $v_t^{orth}$，并通过衰减正交分量来抑制突变：
   
$$
v_t^{reg} = v_t^{proj} + \gamma \cdot v_t^{orth}, \quad \gamma < 1
$$

   正则化后的速度 $v_t^{reg}$ 用于替代原始 $v_t$ 进行下一步的潜在更新，保证迭代过程的平滑和稳定。

5. **目标视频迭代生成**  
   在完整的 50 步去噪过程中，**仅前 10 步**应用流引导优化：每一步使用 Adam 优化器（学习率 0.003，3 次优化迭代）基于 $\mathcal{L}_{FG}$ 更新目标潜在 $z_t$，然后使用正则化速度进行下一步去噪。后续 40 步正常执行流匹配去噪，最终解码得到目标视频。

### 模块间的因果依赖

上述模块形成了一条清晰的因果链：**前向加噪的免反演设计**使运动表示提取无需迭代优化，降低了预处理成本；**基于输出潜在预测的运动表示**使流引导损失的梯度传播完全绕开模型内部层，这是内存开销从 93.1G 骤降至 19.3G 的根本原因（Table 4）；**速度正则化**则作为优化过程的稳定器，消除因仅依赖损失驱动而导致的剧烈波动——消融实验（Table 3）显示，去除速度正则化后运动保真度从 0.850 降至 0.809，时间一致性从 0.986 降至 0.968，画面出现严重退化。

整个框架的设计使 FlowMotion 天然具备**骨干网络无关性**：由于流引导仅依赖模型的速度预测输出，无需知晓内部结构是 U-Net 还是 DiT，因此可无缝适配 Wan2.1‑1.3B 和 Wan2.2‑5B 等不同规模的流匹配 T2V 模型（Figure 6）。

### 补充图表

![[assets/figures/papers/paper_list_l3_https_openaccess_thecvf_com_content_CVPR2026_html_Wang_FlowMotion_Traini/figures/002_Figure_2.jpg]]
*Figure 2: Guidance process of exisiting methods and FlowMotion*



### 3.1 基于流的生成建模背景

FlowMotion 构建在基于流的文本到视频（T2V）生成模型之上。这类模型直接在潜在空间中进行生成建模，其核心是训练一个速度预测网络 $v_\theta$，学习从纯噪声 $z_1 \sim \mathcal{N}(0,1)$ 到干净潜在 $z_0$ 的恒定速度场。训练目标为流匹配损失：

$$\mathcal{L}_{\mathrm{FM}} = \mathbb{E}_{z_0 \sim \mathcal{E}(x), z_1 \sim \mathcal{N}(0,1), t} \left[ \| v_\theta(z_t, t) - (z_1 - z_0) \|_2^2 \right] \tag{1}$$

其中 $z_t = t z_1 + (1-t) z_0$ 为时间 $t$ 处的线性插值潜在，$v_\theta(z_t, t)$ 为模型预测的速度。推理时，从 $z_1$ 出发，利用预测速度逐步去噪以生成干净潜在。

### 3.2 运动表示提取：潜在预测

FlowMotion 的核心创新在于**直接利用模型输出的速度预测来构造运动表示**，而非访问模型内部层。给定当前噪声潜在 $z_t$ 和模型预测速度 $v_t = v_\theta(z_t, t)$，可通过一步线性外推估计对应的干净潜在，称为**潜在预测**（latent prediction）：

$$\hat{z}_0(t) = z_t - t v_t \tag{2}$$

对于源视频，首先将其编码为干净潜在 $z_0^{src}$，然后通过前向加噪过程获得各时间步的噪声潜在 $z_t^{src}$。使用**空提示**（null text prompt）调用模型获得源视频的速度预测 $v_t^{src}$，进而提取源运动表示：

$$\hat{z}_0^{src}(t) = z_t^{src} - t v_t^{src} \tag{3}$$

这一设计的核心洞察在于：早期去噪步骤的潜在预测天然编码了丰富的时空动态信息——从粗粒度的运动轨迹逐步演化为细粒度的动作细节（Figure 3 可视化验证了这一点），且整个过程无需迭代反演，也无需访问模型内部特征。

![[assets/figures/papers/paper_list_l3_https_openaccess_thecvf_com_content_CVPR2026_html_Wang_FlowMotion_Traini/figures/003_Figure_3.jpg]]
*Figure 3: The visualization of latent prediciton: (a) During T2V generation. (b) Extracted from source video*

### 3.3 流引导损失

流引导（flow guidance）的核心思想是对齐源视频与目标生成视频的潜在预测，从而将源视频的运动模式迁移至目标视频。引导损失由两项组成：

**潜在对齐（Latent Alignment, LA）**：直接最小化源与目标视频潜在预测之间的 $\ell_2$ 距离，确保整体运动模式一致。

**差异对齐（Difference Alignment, DA）**：计算相邻帧潜在预测之间的差异，并最小化源与目标视频帧间差异的 $\ell_2$ 距离，以显式保留帧间动态变化。

完整的流引导损失为：

$$\mathcal{L}_{FG} = \alpha \| \hat{z}_0^{src}(t) - \hat{z}_0(t) \|_2^2 + \beta \| \triangle(\hat{z}_0^{src}(t)) - \triangle(\hat{z}_0(t)) \|_2^2 \tag{5}$$

其中 $\triangle(\cdot)$ 表示帧间差分操作，$\alpha$ 和 $\beta$ 为两项损失的权重系数。消融实验（Table 3）证实，去除差异对齐（w/o DA）会导致运动保真度从 0.850 降至 0.842，并引入视觉伪影；仅靠潜在对齐不足以完整保留帧间动态变化。

### 3.4 速度正则化

在迭代优化过程中，目标潜在变量的更新可能出现剧烈波动，导致生成画面退化。FlowMotion 引入**速度正则化**（velocity regularization）来稳定优化过程。

首先计算从初始噪声 $z_1$ 到当前潜在 $z_t$ 的平均流方向，作为正则化的参考基准：

$$v_t^{avg} = \frac{z_t - z_1}{t - 1} \tag{6}$$

然后将当前预测速度 $v_t$ 分解为沿 $v_t^{avg}$ 方向的投影分量 $v_t^{proj}$ 和正交分量 $v_t^{orth}$：

$$v_t^{proj} = \frac{v_t \cdot v_t^{avg}}{\|v_t^{avg}\|_2^2} v_t^{avg}, \quad v_t^{orth} = v_t - v_t^{proj} \tag{7}$$

通过衰减正交分量来抑制突变，生成正则化速度：

$$v_t^{reg} = v_t^{proj} + \gamma \cdot v_t^{orth} \tag{8}$$

其中 $\gamma \in [0, 1]$ 为衰减系数。消融实验（Table 3）表明，去除速度正则化（w/o VR）后运动保真度骤降至 0.809，时间一致性从 0.986 降至 0.968，画面质量严重退化，证实了该模块对优化稳定性的关键作用。

### 3.5 梯度传播路径的关键差异

与传统训练无关方法（如 MotionClone、MOFT、DiTFlow）相比，FlowMotion 的流引导损失完全基于模型输出（速度预测 $v_t$）计算，梯度回传仅涉及潜在变量 $z_t$ 自身，**无需穿透模型内部层**。这一设计带来两个关键优势：

- **极低的资源消耗**：GPU 显存需求仅为 19.3G，几乎接近纯推理开销（17.7G），而基于内部特征的方法（如使用时间注意力图）需 93.1G 甚至超出显存（OOM）（Table 4）。
- **骨干网络无关性**：由于不依赖 U-Net 或 DiT 的特定内部结构，FlowMotion 可无缝适配不同骨干网络，如 Wan2.1-1.3B 和 Wan2.2-5B（Figure 6）。

![[assets/figures/papers/paper_list_l3_https_openaccess_thecvf_com_content_CVPR2026_html_Wang_FlowMotion_Traini/figures/009_Table_4.jpg]]
*Table 4: Memory requirment of different guidance term*



## 实验与关键发现

### 主结果与定量对比

FlowMotion在运动迁移的核心指标上全面超越现有训练无关及训练方法。在50段视频的测试集上，FlowMotion取得了**0.850的运动保真度**（Motion Fidelity）和**0.986的时间一致性**（Temporal Consistency），两项指标均位列所有对比方法之首（Table 1）。这一优势在用户研究中得到进一步验证：FlowMotion获得最高综合评分**4.446**，显著优于基于内部特征引导的训练无关方法（如**MotionClone**、**MOFT**）以及需要微调的训练方法（如**MotionDirector**、**MotionInversion**）（Table 2）。

![[assets/figures/papers/paper_list_l3_https_openaccess_thecvf_com_content_CVPR2026_html_Wang_FlowMotion_Traini/figures/008_Table_2.jpg]]
*Table 2: Average score of user study*

从定性结果来看（Figure 5），FlowMotion能够准确迁移源视频中的运动模式——包括单/多目标运动、相机轨迹和复杂动作——同时保持目标视频的文本语义和背景结构。相比之下，基于时间注意力图或扩散特征的方法在复杂运动场景下常出现运动漂移或纹理伪影（红框标注区域），而FlowMotion得益于直接利用模型输出预测进行引导，避免了内部特征提取引入的噪声和不稳定性。

![[assets/figures/papers/paper_list_l3_https_openaccess_thecvf_com_content_CVPR2026_html_Wang_FlowMotion_Traini/figures/005_Figure_5.jpg]]
*Figure 5: Qualitative comparison with SOTA methods. Red boxes indicated low quality content across frames*

### 跨骨干泛化能力

流引导完全基于模型输出（速度预测）计算，梯度回传仅涉及潜在变量自身，无需访问U-Net或DiT的内部结构。这一设计使FlowMotion可无缝适配不同骨干网络：在**Wan2.1-1.3B**和**Wan2.2-5B**两个参数量差异显著的flow-based T2V模型上，FlowMotion均能生成高质量的运动迁移结果（Figure 6），展示了强泛化能力。而依赖内部特征的方法（如**DiTFlow**、**SMM**）在切换骨干时往往需要重新设计特征提取路径，甚至无法兼容不同架构。

![[assets/figures/papers/paper_list_l3_https_openaccess_thecvf_com_content_CVPR2026_html_Wang_FlowMotion_Traini/figures/007_Figure_6.jpg]]
*Figure 6: Qualitative results of FlowMotion. The left column generated by Wan2.1-1.3B, while right column generated by Wan2.2-5B*

### 资源效率分析

FlowMotion的核心增效在于完全消除了对内部层梯度传播的依赖。Table 4的显存对比揭示：基于内部特征引导的方法（如时间注意力图）需要**93.1G**甚至超出显存（OOM），而FlowMotion仅需**19.3G**，几乎接近纯推理开销（**17.7G**），额外消耗仅1.6G。这一极低的资源需求使FlowMotion可在消费级GPU上完成运动迁移，大幅降低了使用门槛。

### 消融实验：关键模块的贡献

消融实验（Table 3; Figure 7）系统验证了流引导损失中两个组件的不可或缺性：

![[assets/figures/papers/paper_list_l3_https_openaccess_thecvf_com_content_CVPR2026_html_Wang_FlowMotion_Traini/figures/010_Table_3.jpg]]
*Table 3: Ablation results of different key designs*

![[assets/figures/papers/paper_list_l3_https_openaccess_thecvf_com_content_CVPR2026_html_Wang_FlowMotion_Traini/figures/011_Figure_7.jpg]]
*Figure 7: The visualization of ablation on key designs. Red boxes indicate low quality content across frames*

- **去除差异对齐（w/o DA）**：仅保留潜在对齐损失时，运动保真度从0.850降至**0.842**，时间一致性从0.986降至**0.981**，视觉上出现帧间运动不连贯和伪影（Figure 7红框区域）。这表明仅靠帧级潜在对齐无法完整保留源视频的帧间动态变化模式，差异对齐对于捕获运动的时间结构至关重要。

- **去除速度正则化（w/o VR）**：去除正则化后性能出现严重退化——运动保真度骤降至**0.809**，时间一致性降至**0.968**，文本相似度也从0.347降至**0.313**。Figure 7的定性结果显示，无正则化时优化过程出现剧烈波动和过拟合，导致画面严重退化。速度正则化通过将当前速度分解为沿累积流方向的投影分量与正交分量，并衰减正交分量来抑制突变，是保证迭代优化稳定性的关键机制。

### 运动表示选择的权衡

进一步的消融探索（Figure 8）揭示了运动表示选择中的固有权衡：将源运动表示从预测潜在（$\hat{z}_0^{src}(t)$）替换为源视频的干净潜在（$z_0^{src}$）可提升精细动作的迁移精度，但会降低文本对齐程度和背景多样性。这是因为干净潜在包含完整的源视频内容信息，在迁移运动的同时也“泄露”了源视频的外观和背景，削弱了目标提示对生成内容的控制力。这一发现揭示了运动-内容解耦的进一步优化空间。

### 局限性与待验证问题

尽管FlowMotion在运动保真度和资源效率上表现突出，仍存在以下局限需要关注：

1. **文本感知运动的局限性**：源运动表示通过空提示（empty prompt）提取速度预测，可能丢失与特定文本提示相关的运动细节，限制了在需要文本感知运动场景中的性能。这一假设的严格性有待进一步验证。

2. **超参数敏感性**：流程中多个超参数（$\alpha$、$\beta$、$\gamma$、优化步数、学习率等）需针对不同骨干和场景进行调整，目前尚未实现自适应调参。损失权重$\alpha$与$\beta$以及正则化系数$\gamma$对性能的敏感度需要更系统的分析。

3. **模型泛化边界**：当前方法仅在Wan系列flow-based T2V模型上验证，尚未在其他同类模型（如Hunyuan Video）上测试，泛化性有待进一步确认。

4. **优化步数的自适应选择**：当前固定在前10步进行优化，但早期去噪步骤中哪几步对运动迁移最为关键，能否自适应确定最优步数范围，仍是开放问题。



## 定位与知识库关联

### 训练无关运动迁移方法的演进脉络

视频运动迁移的核心目标是：给定一段源视频和一条目标文本描述，生成一段保留源视频运动模式但语义内容与目标文本对齐的新视频。根据是否需要针对特定运动模式进行额外训练，现有方法可分为**训练方法**与**训练无关方法**两大阵营。

**训练方法**通过在单段或多段源视频上微调预训练T2V模型来捕获运动模式。代表性工作包括：**MotionDirector**（Zhao et al., ECCV 2024）通过LoRA（Hu et al., ICLR 2022）微调时间注意力层来学习运动与外观的解耦表示；**MotionInversion**（Wang et al., SIGGRAPH 2025）利用反演技术从源视频中提取运动先验并注入生成过程；**DeT**（Shi et al., arXiv 2025）探索了基于DiT架构的运动解耦策略。这些方法通常能取得较高的运动保真度，但代价是每段新视频都需要数十分钟的微调时间，且微调后的权重仅适用于特定运动模式，缺乏灵活性。

**训练无关方法**则试图在不更新模型参数的前提下完成运动迁移，其核心挑战在于如何从预训练模型中提取有效的运动表示作为引导信号。现有训练无关方法普遍采用“内部特征提取”范式：从T2V模型的时间注意力图、扩散特征或交叉帧注意力流中提取运动线索，然后通过反向传播将这些线索注入目标视频的生成过程。典型代表包括：**MotionClone**（Ling et al., arXiv 2024）利用时间注意力图进行运动克隆；**MOFT**（Xiao et al., NeurIPS 2024）通过扩散特征对齐实现少步运动迁移；**SMM**（Yatim et al., CVPR 2024）探索了基于注意力流的运动匹配；**DiTFlow**（Pondaven et al., CVPR 2025）针对DiT架构设计了专用的内部特征引导机制。

### FlowMotion在方法谱系中的定位

FlowMotion提出的**输出端流引导**范式从根本上改变了运动表示的提取位置：不再深入模型内部层，而是直接利用基于流的T2V模型在输出端产生的速度预测（velocity prediction）来构建运动表示。这一设计选择带来了三个层面的结构性优势：

1. **梯度传播路径的简化**：流引导损失仅依赖于模型输出的速度预测，梯度回传只需经过潜在变量自身，完全绕过了U-Net或DiT的内部参数。这使得GPU显存需求从内部特征方法的93.1G乃至OOM（超出显存）骤降至19.3G，几乎接近纯推理开销（17.7G）（Table 4）。

2. **架构无关性**：由于不依赖特定中间层的特征格式，FlowMotion可无缝适配不同骨干网络。实验验证了该方法在Wan2.1-1.3B和Wan2.2-5B两个参数量差异显著的模型上均能稳定工作（Figure 6），而基于内部特征的方法通常与特定架构紧耦合（如U-Net方法无法直接迁移至DiT骨干）。

3. **运动表示的自然层级**：潜在预测（latent prediction）$\hat{z}_0(t) = z_t - t v_t$ 在早期去噪步骤中天然编码了从粗粒度轨迹到细粒度动作的时空动态信息（Figure 3），无需额外设计复杂的多尺度特征提取机制。

### 适用边界与局限

尽管FlowMotion在运动保真度（0.850）和时间一致性（0.986）上全面超越所有对比方法（Table 1），并在用户研究中获得最高综合评分4.446（Table 2），其适用边界仍需审慎界定：

**架构依赖**：当前方法仅在Wan系列flow-based T2V模型上验证，尚未在其他同类模型（如Hunyuan Video）上测试。虽然流引导的原理不限于特定模型，但不同flow-based模型的速度预测质量和潜在空间结构可能存在差异，泛化性有待进一步确认。

**运动-内容权衡**：源运动表示通过空提示（empty prompt）提取速度预测，这虽然保证了运动提取的纯粹性，但也可能丢失与特定文本提示相关的运动细节。消融实验中的一项探索性发现揭示了这一固有权衡：若将运动表示从预测潜在替换为源视频的干净潜在$z_0^{src}$，可提升精细动作的迁移精度，但会降低文本对齐程度和背景多样性（Figure 8）。这表明运动保真度与文本对齐之间存在尚未完全解耦的张力。

**超参数敏感性**：流程中多个超参数（流引导损失权重$\alpha$与$\beta$、速度正则化系数$\gamma$、优化步数、学习率等）需针对不同骨干和场景进行调整，尚未实现完全自动化。消融实验表明，去除差异对齐（DA）后运动保真度从0.850降至0.842并引入视觉伪影，去除速度正则化（VR）后保真度骤降至0.809且时间一致性从0.986降至0.968（Table 3），说明各模块对超参数配置的依赖性较强。

### 开放问题

FlowMotion的开源设计为后续研究留下了若干值得深入探索的方向：

1. **自适应优化步数**：当前固定在前10步去噪过程中进行优化，但早期步骤中哪几步对运动迁移最为关键？能否根据源视频的运动复杂度自适应地确定最优步数范围？

2. **空提示速度预测的完备性**：空提示提取的速度预测在多大程度上能捕获完整的运动线索？是否存在因缺少文本引导而丢失提示相关动态（如“跳跃”vs“行走”的细微差异）的情况？

3. **损失权重的自适应策略**：$\alpha$与$\beta$的比例以及正则化系数$\gamma$对性能的敏感度如何？是否存在一个简单的自适应调整策略（如基于运动幅度或帧间差异的统计量）来减少人工调参负担？

4. **速度正则化的推广**：速度正则化策略通过将当前速度分解为沿累积流方向的投影分量与正交分量并衰减后者来抑制突变，这一机制能否推广到其他类型的flow-based生成模型（如基于流匹配的图像生成或3D生成模型）？

5. **更自适应的潜在级引导**：能否设计更精细的潜在级引导机制，在保持运动保真度的同时进一步提升文本对齐和背景多样性？例如，对不同空间区域或时间片段施加差异化的引导强度，或引入轻量级的文本感知运动解耦模块。



## 原文 PDF

![[paperPDFs/CVPR_2026/FlowMotion_Training_Free_Flow_Guidance_for_Video_Motion_Transfer.pdf]]
